# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Part 1 - Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the training set
dataset_train = pd.read_csv('Google_Stock_Price_Train.csv')
training_set = dataset_train.iloc[:, 1:2].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
training_set_scaled = sc.fit_transform(training_set)

# Creating a data structure with 60 timesteps and 1 output
X_train = []
y_train = []
for i in range(60, 1258):
    X_train.append(training_set_scaled[i-60:i, 0])
    y_train.append(training_set_scaled[i, 0])
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Part 2 - Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV

# Tuning the RNN

def build_regressor(optimizer):

   regressor = Sequential()
   regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], 1)))
   regressor.add(Dropout(0.2))
   regressor.add(LSTM(units = 50, return_sequences = True))
   regressor.add(Dropout(0.2))
   regressor.add(LSTM(units = 50, return_sequences = True))
   regressor.add(Dropout(0.2))
   regressor.add(LSTM(units = 50))
   regressor.add(Dropout(0.2))
   regressor.add(Dense(units = 1))
   regressor.compile(optimizer = optimizer, loss = 'mean_squared_error')
   return regressor

model_regressor = KerasRegressor(build_fn = build_regressor)

parameters = {'batch_size': [32],
              'epochs': [100],
              'optimizer': ['adam', 'rmsprop']}

grid_search = GridSearchCV(estimator = model_regressor,

                           param_grid = parameters,
                           scoring = 'neg_mean_squared_error',
                           cv = 10)

grid_search = grid_search.fit(X_train, y_train)
best_parameters = grid_search.best_params_
best_accuracy = grid_search.best_score_