"""
Created on March 5 2019

@author: Melchior du Lac
@description: REST+RQ version of RP2paths

"""
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api
import io
import json
import time
import tarfile
import logging


from rp2paths import run


def main(rp2_pathways, timeout):
    with open(rp2_pathways, 'rb') as rp2_pathways_bytes:
        result = run(rp2_pathways_bytes, timeout)
        #app.logger.info(result)
        if result[2]==b'filenotfounderror':
            logging.error('ERROR: FileNotFound Error from rp2paths')
            return False
        elif result[2]==b'oserror':
            logging.error('ERROR: rp2paths has generated an OS error')
            return False
        elif result[2]==b'memerror':
            logging.error('ERROR: Memory allocation error')
            return False
        elif result[0]==b'' and result[1]==b'':
            logging.error('ERROR: Could not find any results by RetroPath2.0')
            return False
        elif result[2]==b'valueerror':
            logging.error('ERROR: Could not setup a RAM limit')
            return False
        out_paths = io.BytesIO(result[0])
        out_compounds = io.BytesIO(result[1])
        return out_paths, out_compounds


#######################################################
############## REST ###################################
#######################################################


app = Flask(__name__)
api = Api(app)


## Stamp of rpCofactors
#
#
def stamp(data, status=1):
    appinfo = {'app': 'RetroPath2.0', 'version': '8.0',
               'author': 'Melchior du Lac',
               'organization': 'BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


## REST App.
#
#
class RestApp(Resource):
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


## REST Query
#
# REST interface that generates the Design.
# Avoid returning numpy or pandas object in
# order to keep the client lighter.
class RestQuery(Resource):
    def post(self):
        outTar = None
        rp2_pathways_bytes = request.files['rp2_pathways'].read()
        params = json.load(request.files['data'])
        conn = Redis()
        q = Queue('default', connection=conn, default_timeout=params['timeout']+10)
        #pass the cache parameters to the rpCofactors object
        async_results = q.enqueue(run, rp2_pathways_bytes, params['timeout'])
        result = None
        while result is None:
            result = async_results.return_value
            if async_results.get_status()=='failed':
                app.logger.error('ERROR: Job failed')
                raise(400)
            time.sleep(2.0)
        #app.logger.info(result)
        if result[2]==b'filenotfounderror':
            app.logger.error('ERROR: FileNotFound Error from rp2paths')
            raise(400)
        elif result[2]==b'oserror':
            app.logger.error('ERROR: rp2paths has generated an OS error')
            raise(400)
        elif result[2]==b'memerror':
            app.logger.error('ERROR: Memory allocation error')
            raise(400)
        elif result[0]==b'' and result[1]==b'':
            app.logger.error('ERROR: Could not find any results by RetroPath2.0')
            raise(400)
        elif result[2]==b'valueerror':
            app.logger.error('ERROR: Could not setup a RAM limit')
            raise(400)
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
    app.run(host="0.0.0.0", port=8992, debug=True, threaded=True)
