# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:17:17 2019

@author: Jean
"""

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
import sys
sys.path.insert(0, './lib')
import model

app = Flask(__name__)
from gevent.pywsgi import WSGIServer

api = Api(app)

model = model.MLModel()

clf_path = 'lib/models/Classifier.pkl'
with open(clf_path, 'rb') as f:
    model.clf = pickle.load(f)

prepos_path = 'models/preprocessing.pkl'
with open(prepos_path, 'rb') as f:
    model.preprocess = pickle.load(f)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


class PredictML(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']

        # preprocessing the user's query and make a prediction
        uq_preprocess = model.numericalImputer_transform(np.array([user_query]))
        prediction = model.predict(uq_preprocess)
        pred_proba = model.predict_proba(uq_preprocess)


        # round the predict proba value and set to new variable
        confidence = round(pred_proba[0], 3)

        # create JSON object
        output = {'prediction': str(prediction), 'probability': confidence}

        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictML, '/prediction')


if __name__ == '__main__':
    #app_server = WSGIServer(('', 4002), app)
    #app_server.serve_forever()
    #app_server.stop()
    #from waitress import serve
    #serve(app, host='localhost', port=4002)
    app.run(host='0.0.0.0', port=4002, debug=True)
    
