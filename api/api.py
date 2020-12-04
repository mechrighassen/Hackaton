import pandas as pd

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from sklearn import svm
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from trainer.build_model import build_model
import gc
import json
import mysql.connector
import os
import pickle
import requests

app = Flask(__name__)
CORS(app)


with open(".database-credential.json", 'r') as json_file:
    database_credential = json.load(json_file)

def csv_to_json(filename, header=None):
        data = pd.read_csv(filename, header=header)
        return data.to_dict('records')

def connect_to_mysql():
    return mysql.connector.connect(
        host=database_credential["host"],
        user=database_credential["user"],
        passwd=database_credential["password"],
        database=database_credential["database"],
    )
    
    
@app.route('/split', methods=['GET'])
def split():
    req_data = request.args
    model_name = req_data['split']
    print(model_name)
    build_model(float(model_name))
    return 'sucess'


@app.route('/', methods=['GET'])
def welcome():
    res = jsonify({"status": "success", "data": "Your api is working"})
    res.status_code = 200
    mydb = connect_to_mysql()
    try:
        mycursor = mydb.cursor()
        mycursor.execute("CREATE TABLE MODELS (parameteres VARCHAR(255), algorithmes VARCHAR(255), id VARCHAR(255) , path VARCHAR(255), PRIMARY KEY(id))")
    except Exception:
        return 'error table MODELS already exists'

    return res


"""pour recuperer les donnees de la base SQL pour un id """
def get_data_sql(user_id):
    mydb = connect_to_mysql()
    mycursor = mydb.cursor()
    mycursor.execute('''SELECT * FROM MODELS WHERE id='''+str(user_id))
    rv = mycursor.fetchall()
    #payload = []
    content = {}
    for result in rv:
        content = {'parameteres': result[0], 'algorithmes': result[1], 'id':result[2], 'path':result[3]}
    print(content)
    return content

""" compte le nombre de modeles """
def count_sql():
    mydb = connect_to_mysql()
    mycursor = mydb.cursor()
    mycursor.execute('''SELECT COUNT(*) FROM MODELS''')
    rv = mycursor.fetchall()
    return rv[0][0]

""" entrainement du modele et enregistrement du modele"""
@app.route('/model/<Id>/train', methods=['POST'])
def train(Id):
    Id = Id
    content = get_data_sql(Id)
    #param = content.get('parameteres')
    algo = content.get('algorithmes')
    req_data = request.json
    path_db = req_data['path_db']   #lib/data/train.csv"
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, path_db)
    data = pd.read_csv(file_res)
    y = data[data.columns[-1]]
    X = data.drop(data.columns[-1], axis=1)
    if not os.path.exists('models'):
        os.mkdir('models')

    nom= algo + str(Id)
    score, X, y=build_model(True,X,y,0.3,nom,algo)
    mydb = connect_to_mysql()
    path='models/'+ nom +'.pkl'
    mycursor = mydb.cursor()
    sql = "UPDATE MODELS SET path='"+path+"' where id="+str(Id)
    mycursor.execute(sql)
    mydb.commit()
    post_data = {}
    post_data['Success']= 'True'
    post_data['precision']= str(score)
    return str(post_data)
#localhost:5000/model/1/train

""" prediction a partir d'un modele deja present"""
@app.route('/model/<Id>/predict', methods=['POST'])
def predict(Id):
    Id = Id
    req_data = request.json
    path_db = req_data['path_db']
    content = get_data_sql(Id)
    #split = content.get('parameteres')
    path_pkl=content.get('path')
    algo = content.get('algorithmes')
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, path_db)

    data = pd.read_csv(file_res)     
    X=data   
    y=None
    nom= algo + str(Id)
    #On applique le pre-traitement
    score, X, y=build_model(False,X,y,0.2,nom,algo)
    
    loaded_model = pickle.load(open(path_pkl, 'rb'))
    pred = loaded_model.predict(X)
    post_data = {}
    post_data['Success']= 'True'
    post_data['prediction']= pred
    return str(post_data)
#localhost:5000/model/1/predict    


@app.route('/add_user', methods=['POST'])
def add_user():
    req_data = request.json
    name = req_data['name']
    password = req_data['password']
    email = req_data['email']
    id = req_data['id']
    mydb = connect_to_mysql()
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO USERS (name, email, password, id) VALUES (%s, %s, %s, %s)"
        val = (name,password,email,id)
        mycursor.execute(sql,val)
        mydb.commit()
    except Exception:
        return 'error key already exists'
    return "sucess"


@app.route('/users/<user_id>', methods = ['GET', 'POST', 'DELETE'])
def user(user_id):
    mydb = connect_to_mysql()
    if request.method == 'GET':
        """return the information for <user_id>"""
        mycursor = mydb.cursor()
        mycursor.execute('''SELECT * FROM USERS WHERE id='''+str(user_id))
        rv = mycursor.fetchall()
        payload = []
        content = {}
        for result in rv:
            content = {'name': result[0], 'email': result[1], 'password': result[2], 'id':result[3]}
            payload.append(content)
            content = {}
        return jsonify(payload)
        #mycursor.execute(sql)

    if request.method == 'POST':
        """modify/update the information for <user_id>"""
        req_data = request.json # a multidict containing POST data
        name = req_data['name']
        password = req_data['password']
        email = req_data['email']
        try:
            mycursor = mydb.cursor()
            sql = "UPDATE USERS SET name='"+name+"', password='"+password+"', email='"+email+"' where id="+str(user_id)
            print(sql)
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            print(e)
            return 'POST error'
        return 'sucess'

    if request.method == 'DELETE':
        """delete user with ID <user_id>"""
        mycursor = mydb.cursor()
        sql = "DELETE FROM USERS WHERE id=" + str(user_id)
        mycursor.execute(sql)
        mydb.commit()
        return 'sucess'
    else:
        # POST Error 405 Method Not Allowed
        return 'Error else'


@app.route('/model/add', methods=['POST'])
def add():
    '''
    example of input JSON FILE : {"id": 1,"parameteres":"[0.1, lin]" ,"algorithmes":"LogisticRegression Model" }
    :return:
    JSON FILE
    '''
    req_data = request.json
    algorithmes = req_data['algorithmes']
    #parameteres = req_data['parameteres']
    parameteres = None
    if parameteres != None:
        parameteres = ','.join(str(x) for x in parameteres)
    #path = 'NULL'
    mydb = connect_to_mysql()
    data = {}
    try:
        mycursor = mydb.cursor()
        sql = "SELECT MAX(id) FROM MODELS"
        mycursor.execute(sql)
        rv = mycursor.fetchall()
        id = rv[0][0]
        if id!=None:
            id = int(rv[0][0])+1
        else:
            id = 0
        mycursor = mydb.cursor()
        sql = "INSERT INTO MODELS (parameteres, algorithmes, id) VALUES (%s, %s, %s)"
        val = (parameteres, algorithmes, id)
        mycursor.execute(sql, val)
        mydb.commit()
        data['id'] = id
        data['Success'] = True
        return data
    except Exception as e:
        data['Success'] = False
        return data


@app.route('/model/<model_id>', methods = ['GET', 'POST', 'DELETE'])
def model_edit(model_id):
    mydb = connect_to_mysql()
    if request.method == 'GET':
        """return the information for <model_id>"""

        mycursor = mydb.cursor()
        mycursor.execute('''SELECT * FROM MODELS WHERE id='''+model_id)
        rv = mycursor.fetchall()
        payload = []
        content = {}
        for result in rv:
            content = {'parameteres': result[0], 'algorithmes': result[1], 'id': result[2], 'path':result[3]}
            content['Success'] = True
            payload.append(content)
            content = {}
        return jsonify(payload)

    if request.method == 'POST':
        """modify/update the information for <model_id>"""
        req_data = request.args # a multidict containing POST data
        parameteres = req_data['parameteres']
        algorithmes = req_data['algorithmes']
        data = {}
        try:
            mycursor = mydb.cursor()
            sql = "UPDATE MODELS SET parameteres='"+parameteres+"', algorithmes='"+algorithmes+"' where id="+str(model_id)
            mycursor.execute(sql)
            mydb.commit()
            data['Success'] = True
            return data
        except Exception as e:
            data['Success'] = False
            print(e)
            return data

    if request.method == 'DELETE':
        data = {}
        try:
            """delete model with ID <model_id>"""
            mycursor = mydb.cursor()
            sql = "DELETE FROM MODELS WHERE id=" + str(model_id)
            mycursor.execute(sql)
            mydb.commit()
            data['Success'] = True
            return data
        except Exception:
            data['Success'] = False
            return data
    else:
        # POST Error 405 Method Not Allowed
        data = {}
        data['Success'] = False
        return data

@app.route('/model', methods=['GET'])
def model():
    mydb = connect_to_mysql()
    mycursor = mydb.cursor()
    mycursor.execute('''SELECT * FROM MODELS''')
    rv = mycursor.fetchall()
    payload = []
    content = {}
    for result in rv:
        content = { 'parameteres': result[0], 'algorithmes': result[1], 'id': result[2],'path':result[3]}
        payload.append(content)
    return jsonify(payload)

app.run()
