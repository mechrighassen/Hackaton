from lib.model import MLModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn.metrics import accuracy_score

""" Pre-traitement + train du modele et enregistrement du modele sous format .pkl """
""" train = boolean, Si train=False alors on fait que le pre-traitement"""
def build_model(train,X,y,split,Id,algo):
    model = MLModel(algo)
        
    for feature in X :
        if X[feature].dtypes==object :
            model.categoricalFill_fit(X)
            X[feature]=model.categoricalFill_transform(X[feature])
            X[feature]=model.categoricalImputer_transform(X[feature])

            
    for feature in X.columns :
        X[feature] = model.numericalImputer_transform(X[feature])
    print('Preprocessing transform complete')
    score = 0

    if train==True:
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=42)
        model.train(X_train, y_train)
        print('Model training complete')
    
        y_pred = model.predict(X_test)
        score=accuracy_score(y_test,y_pred)
        print(score)
        model.pickle_clf(Id)
    
    return score, X, y


#if __name__ == "__main__":
    #build_model(0.3)
