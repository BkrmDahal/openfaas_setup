# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request
from function import handler
#from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIServer
from keras.models import load_model
try:
    from utils import read_config
except:
    from function.utils import read_config

# get configs
configs = read_config('function/config.yaml')

# load the model
model = load_model('function/'+configs['MODEL_PATH'])
model._make_predict_function()

# flask app name
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_route():
    if request.method == 'GET':
        return """ENDPOINT: /v1/predict \n
                 POST: send json/application with body { \n
                                            "body": "YOUR TEXT",\n
                                            "intel_text": "YOUR TEXT",\n
                                            "headline": "YOUR TEXT",\n
                                            ... \n
                                            }"""

    if request.method == 'POST':
        raw_json = request.get_data()
        try:
            result_json = raw_json.decode('utf-8')
        except Exception as e:
            return {'status':'failed', 'error':e}
        print(raw_json)
        ret = handler.handle(result_json, model)
        
    return ret

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
