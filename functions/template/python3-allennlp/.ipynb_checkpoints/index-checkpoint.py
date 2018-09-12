import josn

from allennlp.models.archival import load_archive
from allennlp.service.predictors import Predictor

def get_predictor(file_path):
    """get the predictor"""
    archive = load_archive(file_path)
    file_type = archive.config.get("model").get("type")
    predictor_cf = Predictor.from_archive(archive, DEFAULT_PREDICTORS[file_type])
    return predictor_cf

## there might be latest model check allennlp website https://allennlp.org/models and repo
# for detail about input format please check https://allennlp.org/models
predictors_ncr = get_predictor("https://s3-us-west-2.amazonaws.com/allennlp/models/ner-model-2018.02.12.tar.gz")
predictors_mc = get_predictor("https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")
predictors_cf = get_predictor("https://s3-us-west-2.amazonaws.com/allennlp/models/coref-model-2018.02.05.tar.gz")

"""setup default value and model"""
DEFAULT_PREDICTORS = {
        'srl': 'semantic-role-labeling',
        'decomposable_attention': 'textual-entailment',
        'bidaf': 'machine-comprehension',
        'simple_tagger': 'sentence-tagger',
        'crf_tagger': 'sentence-tagger',
        'coref': 'coreference-resolution'
        }

# flask app name
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_route():
    if request.method == 'GET':
        return """allenlp"""

    if request.method == 'POST':
        raw_json = request.data
        try:
            result_json = json.loads(raw_json.decode('utf-8'))
            typ = result_json['type']
            del result_json('type')
        except Exception as e:
            return json.dumps({'status':'failed', 'error':e})
        
        if typ=='ncr':
            data = predictor_ncr.predict_json(result_json)
        elif typ=='mc':
            data = predictor_mc.predict_json(result_json)
        elif typ=='cf':
            data = predictor_cf.predict_json(result_json)
        else:
            return json.dumps({'status':'failed', 'error':"type can be only ncr or mc or cf",
                       'type':typ})
        
    return json.dumps({'status':'success',
                    'data':data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

