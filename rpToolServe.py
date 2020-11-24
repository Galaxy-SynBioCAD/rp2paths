"""
Created on March 5 2019

@author: Melchior du Lac
@description: REST+RQ version of RP2paths

"""
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort, Response
from flask_restful import Resource, Api
import io
import json
import time
import tarfile
import logging
import sys
import time

from rq import Connection, Queue
from redis import Redis

import rpTool

#######################################################
############## logging ################################
#######################################################

from logging.handlers import RotatingFileHandler

#######################################################
############## REST ###################################
#######################################################


app = Flask(__name__)
api = Api(app)


def stamp(data, status=1):
    """Default message to return

    :param data: The data to be passes
    :param status: The int value of the status
    
    :type data: dict
    :type status: int

    :rtype: dict
    :return: The dict of the stamp
    """
    appinfo = {'app': 'RP2paths', 'version': '8.0',
               'author': 'Melchior du Lac',
               'organization': 'BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


class RestApp(Resource):
    """The Flask methods that we support, post and get
    """
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


#Note: Avoid returning numpy or pandas object in order to keep the client lighter.
class RestQuery(Resource):
    """Class containing the REST requests for RP2
    """
    def post(self):
        """Make the REST request using the POST method

        :rtype: Response
        :return: Flask Response object 
        """
        outTar = None
        rp2_pathways_bytes = request.files['rp2_pathways'].read()
        params = json.load(request.files['data'])
        ##### REDIS ##############
        conn = Redis()
        q = Queue('default', connection=conn, default_timeout='24h')
        #pass the cache parameters to the rpCofactors object
        async_results = q.enqueue(rpTool.run_rp2paths, rp2_pathways_bytes, params['timeout'])
        result = None
        while result is None:
            result = async_results.return_value
            app.logger.info(async_results.return_value)
            app.logger.info(async_results.get_status())
            if async_results.get_status()=='failed':
                return Response('Job failed \n '+str(result), status=400)
            time.sleep(2.0)
        ########################### 
        if result[2]==b'filenotfounderror':
            app.logger.error("FileNotFound Error from rp2paths \n "+str(result[3]))
            return Response("FileNotFound Error from rp2paths \n "+str(result[3]), status=500)
        elif result[2]==b'oserror':
            app.logger.error("rp2paths has generated an OS error \n"+str(result[3]))
            return Response("rp2paths has generated an OS error \n"+str(result[3]), status=500)
        elif result[2]==b'memoryerror':
            app.logger.error("rp2paths does not have sufficient memory to continue \n"+str(result[3]))
            return Response("rp2paths does not have sufficient memory to continue \n"+str(result[3]), status=403)
        elif result[2]==b'ramerror':
            app.logger.error("Could not setup a RAM limit \n"+str(result[3]))
            return Response("Could not setup a RAM limit \n"+str(result[3]), status=500)
        elif result[2]==b'timeout':
            app.logger.error("rp2paths has reached its timeout limit, try to increase it \n"+str(result[3]))
            return Response("rp2paths has reached its timeout limit \n"+str(result[3]), status=408)
        if result[0]==b'' and result[1]==b'':
            app.logger.error("rp2paths has not found any results and returns empty files \n"+str(result[3]))
            return Response("rp2paths has not found any results and returns empty files \n"+str(result[3]), status=400)
        outTar = io.BytesIO()
        with tarfile.open(fileobj=outTar, mode='w:xz') as tf:
            #make a tar to pass back to the rp2path flask service
            out_paths = io.BytesIO(result[0])
            out_compounds = io.BytesIO(result[1])
            info = tarfile.TarInfo(name='rp2paths_pathways')
            info.size = len(result[0])
            tf.addfile(tarinfo=info, fileobj=out_paths)
            info = tarfile.TarInfo(name='rp2paths_compounds')
            info.size = len(result[1])
            tf.addfile(tarinfo=info, fileobj=out_compounds)
        ###### IMPORTANT ######
        outTar.seek(0)
        #######################
        return send_file(outTar, as_attachment=True, attachment_filename='rp2paths_result.tar', mimetype='application/x-tar')



api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    handler = RotatingFileHandler('rp2paths.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
