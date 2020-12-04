# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 12:54:52 2019

@author: Jean
"""

# ML imports
from sklearn import svm
# from sklearn.naive_bayes import BernoulliNB
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn import tree
from sklearn import neighbors
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
import pickle

#from api.trainer.Ann import Ann


class MLModel(object):

    
    def __init__(self, num ,tol=0.05, variables=None):
        if num == 'SVM':
            self.clf = svm.SVC(probability=True)
        if num == 'Random Forest':
            self.clf = RandomForestClassifier(n_estimators=30, max_depth=5,random_state=0)
        if num == 'Linear Regression':
            self.clf = LinearRegression()
        if num == 'Decision Tree Classifier':
            self.clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5)
        if num == 'KNN':
            self.clf = neighbors.KNeighborsClassifier()
        if num == 'One vs Rest Classifier':
            self.clf = OneVsRestClassifier(SGDClassifier())
        if num == 'Gaussian NB':
            self.clf = GaussianNB()
        if num == 'MLP Classifier':
            self.clf = MLPClassifier()
        if num == 'Gaussian Process Classifier':
            self.clf = GaussianProcessClassifier()
        #if num == 9:
            #self.clf = Ann(4, 1, [6, 6, 3]) #classes values must start from 0
        self.tol = tol
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    # Example of preprocessing
    def numericalImputer_fit(self, X, y=None):
        # persist mode in a dictionary
        self.imputer_dict_ = {}
        #for feature in self.variables:
        #if feature != None :
        self.imputer_dict_[X] = X.mean()
        #print("numeric_fit")
        return self

    def numericalImputer_transform(self, X):
        X = X.copy()
        #for feature in self.variables:
        #if feature != None :
        m= X.mean()
        X.fillna(m, inplace=True)
        #print("numeric_trans")
        return X
    
    def categoricalImputer_fit(self, X, y):
        temp = pd.concat([X, y], axis=1)
        temp.columns = list(X.columns) + ['target']

        # persist transforming dictionary
        self.encoder_dict_ = {}

        for var in self.variables:
            if var != None:
                t = temp.groupby([var])['target'].mean().sort_values(ascending=True).index
                self.encoder_dict_[var] = {k: i for i, k in enumerate(t, 0)}
                #print("categ_imput_fit")

        return self

    def categoricalImputer_transform(self, X):
        # encode labels
        X = X.copy()
        #for feature in self.variables:
        #if feature != None:
        li=[]
        for l in X:
            if l not in li:
                li.append(l)
            
        for k in range(X.shape[0]):
            X[k]=li.index(X[k])
        #print("categ_imput_trans")

        
        """
        # check if transformer introduces NaN
        if X[self.variables].isnull().any().any():
            null_counts = X[self.variables].isnull().any()
            vars_ = {key: value for (key, value) in null_counts.items()
                     if value is True}"""
        #print(X)
        return X
    
    def categoricalFill_fit(self, X, y=None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self

    def categoricalFill_transform(self, X):
        X = X.copy()
        #print(self.variables)
        #for feature in self.variables:
        #print(X)
        #if feature != None:
        #print("categfill_trans")
        X = X.fillna('Missing')
        #print(X)

        return X
    
    def categoricalEncoder_fit(self, X, y):
        temp = pd.concat([X, y], axis=1)
        temp.columns = list(X.columns) + ['target']

        # persist transforming dictionary
        self.encoder_dict_ = {}

        for var in self.variables:
            if var != None:
                t = temp.groupby([var])['target'].mean().sort_values(ascending=True).index
                self.encoder_dict_[var] = {k: i for i, k in enumerate(t, 0)}
                #print("categ_encod_fit")

        return self

    def categoricalEncoder_transform(self, X):
        # encode labels
        X = X.copy()
        for feature in self.variables:
            if feature != None :
                X[feature] = X[feature].map(self.encoder_dict_[feature])

        # check if transformer introduces NaN
        if X[self.variables].isnull().any().any():
            null_counts = X[self.variables].isnull().any()
            vars_ = {key: value for (key, value) in null_counts.items()
                     if value is True}
            #raise errors.InvalidModelInputError(
            #    f'Categorical encoder has introduced NaN when '
            #    f'transforming categorical variables: {vars_.keys()}')

        return X

    

    def train(self, X, y):
        """Trains the classifier to associate the label with the sparse matrix
        """
        # X_train, X_test, y_train, y_test = train_test_split(X, y)
        self.clf.fit(X, y)

    def predict_proba(self, X):
        """Returns probability for the classes in a numpy array
        """
        y_proba = self.clf.predict_proba(X)
        return y_proba[:, 1]

    def predict(self, X):
        """Returns the predicted class in an array
        """
        y_pred = self.clf.predict(X)
        return y_pred

    def pickle_preprocess(self,user ,path='models/preprocessing.pkl'):
        path = user+'/'+path
        with open(path, 'wb') as f:
            pickle.dump(self.variables, f)
            print("Pickled preprocessing at {}".format(path))

    def pickle_clf(self,Id, path='models/Classifier'):
        """Saves the trained classifier for future use.
        """
        path = path + str(Id) + '.pkl'
        with open(path, 'wb') as f:
            pickle.dump(self.clf, f)
            print("Pickled classifier at {}".format(path))

    
