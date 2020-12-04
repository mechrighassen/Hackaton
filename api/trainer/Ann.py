# Artificial Neural Network

# Importing the packages
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix
from keras.utils import to_categorical
import numpy as np
import pandas as pd


# Initialising the ANN
class Ann:
    def __init__(self, x_train, y_train, hidden_layers=1, units=[0], kernel_initializer='uniform', activation='relu',
                 optimizer='adam', loss='categorical_crossentropy'):
        # attributes
        self.hidden_layers = hidden_layers
        self.input_dim = x_train.shape[1]
        output_dim = len(list(set(y_train)))
        nodes=(self.input_dim+output_dim)//2
        self.units = units  # list
        if self.units[0] == 0:
            self.units = [nodes, nodes, output_dim]
        self.activation = activation
        self.loss = loss
        self.optimizer = optimizer
        self.kernel_initializer = kernel_initializer
        self.y_ordered = []
        self.sequential = Sequential()

        # Adding the input layer and the first hidden layer
        self.sequential.add(
            Dense(units=self.units[0], kernel_initializer=self.kernel_initializer, activation=self.activation,
                  input_dim=self.input_dim))

        # Adding the other hidden layers
        for i in range(1, hidden_layers + 1):
            self.sequential.add(
                Dense(units=self.units[i], kernel_initializer=self.kernel_initializer, activation=self.activation))

        # Adding the output layer
        if self.units[len(self.units) - 1] == 2:
            self.sequential.add(Dense(units=self.units[len(self.units) - 1], activation='sigmoid'))
        else:
            self.sequential.add(Dense(units=self.units[len(self.units) - 1], activation='softmax'))

        # Compiling the ANN
        self.sequential.compile(self.optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Fitting the ANN to the Training set
    def fit(self, x_train, y_train, batch_size=10, epochs=100):
        y_train = to_categorical(y_train)
        self.sequential.fit(x_train, y_train, batch_size, epochs)

    # Prediction
    def predict(self, x_test):
        return np.argmax(self.sequential.predict(x_test), axis=1)
        

    # confusion_matrix
    def confusion_matrix(self, y_test, y_pred):
        return confusion_matrix(y_test, y_pred)