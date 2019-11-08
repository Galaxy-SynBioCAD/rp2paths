#!/usr/bin/env python3
"""
Created on March 5 2019

@author: Melchior du Lac
@description: REST+RQ version of RP2paths

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api
import io
import json
import time
from rq import Connection, Queue
import tarfile

import rp2paths


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
        with Connection():
            q = Queue(default_timeout=params['timeout']+10)
            rp2_pathways_bytes = request.files['rp2_pathways'].read()
            params = json.load(request.files['data'])
            #pass the cache parameters to the rpCofactors object
            async_results = q.enqueue(rp2paths.run,
                                      rp2_pathways_bytes,
                                      params['timeout'])
            result = None
            while result is None:
                result = async_results.return_value
                time.sleep(2.0)
            #TODO: check that!
            #make a tar to pass back to the rp2path flask service
            out_paths = io.BytesIO(result[0])
            out_compounds = io.BytesIO(result[1])
            outTar = io.BytesIO()
            if not return_content==None or not (return_content[0]==b'' and return_content[1]==b''):
                with tarfile.open(fileobj=outTar, mode='w:xz') as tf:
                    info = tarfile.TarInfo(name='rp2paths_pathways')
                    info.size = len(result[0])
                    tf.addfile(tarinfo=info, fileobj=out_paths)
                    info = tarfile.TarInfo(name='rp2paths_compounds')
                    info.size = len(result[1])
                    tf.addfile(tarinfo=info, fileobj=out_compounds)
            ###### IMPORTANT ######
            outTar.seek(0)
            #######################
        return send_file(outTar, as_attachment=True, attachment_filename='rp2paths_resuts.tar', mimetype='application/x-tar')


api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8992, debug=True, threaded=True)
