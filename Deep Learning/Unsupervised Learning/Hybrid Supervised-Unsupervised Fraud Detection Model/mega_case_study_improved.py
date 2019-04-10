# Mega Case Study - Make a Hybrid Deep Learning Model



# Part 1 - Identify the Frauds with the Self-Organizing Map

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Credit_Card_Applications.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Feature Scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
X = sc.fit_transform(X)

# Training the SOM
from minisom import MiniSom
som = MiniSom(x = 10, y = 10, input_len = 15, sigma = 1.0, learning_rate = 0.5)
som.random_weights_init(X)
som.train_random(data = X, num_iteration = 100)

# Visualizing the results
from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
for i, x in enumerate(X):
    w = som.winner(x)
    plot(w[0] + 0.5,
         w[1] + 0.5,
         markers[y[i]],
         markeredgecolor = colors[y[i]],
         markerfacecolor = 'None',
         markersize = 10,
         markeredgewidth = 2)
show()

# Finding the frauds
rows = 10   # dimensions of SOM
cols = 10
  

# Add indices to SOM values & sort by value
helper = np.concatenate(
    (som.distance_map().reshape(rows*cols, 1),         # the SOM map values
     np.arange(rows*cols).reshape(rows*cols, 1)),      # concatenated with an index
    axis=1)                                            # as a 2D matrix with 2 columns of data
helper = helper[helper[:, 0].argsort()][::-1]          # sort by first column (map values) and reverse (so top values are first)

# First choose how many cells to take as outliers
use_threshold = True   # toggle usage for calculating indices (pick cells that exceed threshold or use hardcoded number of cells)
top_cells = 4          # 4 out of 100 seems a valid idea, but ideally it might be chosen after inspecting the current SOM plot
threshold = 0.8        # Use threshold to select top cells

# Take indices that correspond to cells we're interested in
idx = helper[helper[:, 0] > threshold, 1] if use_threshold else helper[:top_cells, 1]

# Find the data entries assigned to cells corresponding to the selected indices
result_map = []
mappings = som.win_map(X)
for i in range(rows):
    for j in range(cols):
        if (i*rows+j) in idx:
            if len(result_map) == 0:                
                result_map = mappings[(i,j)]
            else:
                # Sometimes a cell contains no observations (customers)... weird
                # This will cause numpy to raise an exception so guard against that!
                if len(mappings[(i,j)]) > 0:
                    result_map = np.concatenate((result_map, mappings[(i,j)]), axis=0)                
 
# finally we get our fraudster candidates
frauds = sc.inverse_transform(result_map)
 
# This is the list of potential cheaters (customer ids)
#print(frauds[:, 0])

# Part 2 - Going from Unsupervised to Supervised Deep Learning

# Creating the matrix of features
customers = dataset.iloc[:, 1:].values

# Creating the dependent variable
is_fraud = np.zeros(len(dataset))
for i in range(len(dataset)):
    if dataset.iloc[i,0] in frauds:
        is_fraud[i] = 1

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
customers = sc.fit_transform(customers)

# Part 2 - Create the ANN!

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

# Adding the input layer and the first hidden layer
classifier.add(Dense(units = 2, kernel_initializer = 'uniform', activation = 'relu', input_dim = 15))

# Adding the output layer
classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compiling the ANN
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Fitting the ANN to the Training set
classifier.fit(customers, is_fraud, batch_size = 1, epochs = 2)

# Predicting the probabilities of frauds
y_pred = classifier.predict(customers)
y_pred = np.concatenate((dataset.iloc[:, 0:1].values, y_pred), axis = 1)
y_pred = y_pred[y_pred[:, 1].argsort()]