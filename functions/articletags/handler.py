import pickle
import os
import shutil
from collections import defaultdict
import logging
import warnings
import yaml
import json
from keras.preprocessing.sequence import pad_sequences
try:
    from utils import read_config, top_n, clean_up_sentence, make_dirs, delete_dirs
except:
    from function.utils import read_config, top_n, clean_up_sentence, make_dirs, delete_dirs

# load config files
configs = read_config('function/config.yaml')


# Load tokenizer and label name from pickles.
with open('function/'+configs['TOKENIZER_LABEL_PICKLE_PATH'], 'rb') as handle:
    tokenizer_label_name = pickle.load(handle)

label_name = tokenizer_label_name['class_name']
tokenizer = tokenizer_label_name['tokenizer']

MAX_SEQUENCE_LENGTH = configs['MAX_SEQUENCE_LENGTH']


def handle(req, model):
                
    # clean text
    text = clean_up_sentence(req)
    text = tokenizer.texts_to_sequences([text])
    data = pad_sequences(text, maxlen=MAX_SEQUENCE_LENGTH)

    # predict the class
    predict = model.predict(data)
    predict  = { label:p for (label, p) in zip(label_name.values(), predict[0])}

    ##predicted calss
    predict = sorted(predict.items(), key=lambda x: x[1])[::-1]

    # get only those predict with probility 0.3
    p = [ (i, j) for i, j in predict if j > configs['threshold_cutoff']]

    # of low probility get top 3
    if len(p) < 3:
        p = [(i, j) for i, j in predict[:3]]
    
    # special case of noah's archive
    prediction = []
    for i, j in p:
        if i=='"noahs archive"':
            prediction.append(("noah's archive", j))
        else:
            prediction.append((i,j))


    # make dict of label and probility
    prediction = [{'tag': i, 'probability':str(j)} for i, j in prediction]

    # make format as of vm
    tags = configs['tags']

    list_dict = defaultdict(list)
    
    for tag in prediction:
        list_dict[tags[tag['tag']]].append(tag)
        
    return json.dumps({'status':'success',
                            'status_code': 200,
                            'signals': dict(list_dict)}  )


