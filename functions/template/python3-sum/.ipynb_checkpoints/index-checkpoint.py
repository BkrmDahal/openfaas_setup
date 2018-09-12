import json

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as sumySummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from gensim.summarization import summarize as gSummarize
from summa import summarizer as summaSummarizer
from flask import Flask, request
import nltk
nltk.download('punkt')

# flask app name
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_route():
    if request.method == 'GET':
        return """Summarizer"""

    if request.method == 'POST':
        raw_json = request.data
        try:
            result_json = json.loads(raw_json.decode('utf-8'))
            body = result_json['body']
            typ = result_json['type']
        except Exception as e:
            return json.dumps({'status':'failed', 'error':e})
        
        if typ=='v1':
            summary = gSummarize(body)
        elif typ=='v2':
            summary = summaSummarizer.summarize(body)
        elif typ=='v3':
            parser = PlaintextParser.from_file(body, Tokenizer('english'))
            stemmer = Stemmer('english')

            summarizer = sumySummarizer('english')
            summarizer.stop_words = get_stop_words('english')

            summary = [i for i in summarizer(parser.document, sentence_count)]

            summary = '. '.join(summary)
        else:
            return json.dumps({'status':'failed', 'error':"type can be only v1 or v2 or v3",
                       'type':typ})
        
    return json.dumps({'status':'success',
                    'summary':summary,
                    'text':body,
                      'type':typ})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
