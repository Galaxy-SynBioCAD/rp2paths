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

import rpTool


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
        result = rpTool.main(rp2_pathways_bytes, params['timeout'])
        #app.logger.info(result)
        if result[0]==b'' and result[1]==b'':
            app.logger.error('Could not find any results by RetroPath2.0')
            raise(400)
        outTar = io.BytesIO()
        with tarfile.open(fileobj=outTar, mode='w:xz') as tf:
            #make a tar to pass back to the rp2path flask service
            #out_paths = io.BytesIO(result[0])
            #out_compounds = io.BytesIO(result[1])
            out_paths = result[0]
            out_compounds = result[1]
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
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
