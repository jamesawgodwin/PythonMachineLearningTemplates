

# Plot ad hoc CIFAR10 instances
from keras.datasets import cifar10
from matplotlib import pyplot
from scipy.misc import toimage
# load data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
# create a grid of 3x3 images
for i in range(0, 9):
	pyplot.subplot(330 + 1 + i)
	pyplot.imshow(toimage(X_train[i]))
# show the plot
pyplot.show()

# Simple CNN model for CIFAR-10
import numpy as np
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
K.set_image_dim_ordering('th')

# fix random seed for reproducibility
seed = 0
np.random.seed(seed)
#load cifar dataset
(X_train, y_train), (X_test, y_test) = cifar10.load_data()
# pixel values in range 0-255 for 3 color channels
#normalize each value by dividing by max observation (255) to create range of 0-1
#cast integers to floating point values to perform division

# normalize inputs from 0-255 to 0.0-1.0
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0
# one hot encode outputs, transform 10 classes into binary matrix of width 10
y_train = np_utils.to_categorical(y_train) #,nb_classes)
y_test = np_utils.to_categorical(y_test) #,nb_classes)
num_classes = y_test.shape[1] #unsure if this works with image augmentation

# =============================================================================
# conv input layer, 32 feature maps with 3x3 size, relu activation, weight constraint of max norm set to 3
#dropout initialized to 20% for input layer
#conv layer, 32 feature maps with size 3x3, relu, max norm 3
#max pool layer with size 2x2
#flatten layer
#fully connected layer with 512 units, relu
#dropout set to 40%
#fully connected layer with 10 units and softmax activation function (because categorical prob - as opposed to binary sigmoid prob )
# =============================================================================

# Create the Classifier
classifier = Sequential()
classifier.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), padding='same', activation='relu', kernel_constraint=maxnorm(3)))
classifier.add(Dropout(0.2))
classifier.add(Conv2D(32, (3, 3), activation='relu', padding='same', kernel_constraint=maxnorm(3)))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
classifier.add(Flatten())
classifier.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
classifier.add(Dropout(0.5))
classifier.add(Dense(num_classes, activation='softmax'))
# Compile model
epochs = 2
lrate = 0.01
decay = lrate/epochs
adm = Adam(lr=lrate, decay=decay)
#sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
classifier.compile(loss='categorical_crossentropy', optimizer=adm, metrics=['accuracy'])
print(classifier.summary())

#image augmentation
from keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

# compute quantities required for featurewise normalization
# (std, mean, and principal components if ZCA whitening is applied)
datagen.fit(X_train)

validation_data=(X_test,y_test)

# fits the model on batches with real-time data augmentation:
classifier.fit_generator(datagen.flow(X_train, y_train, batch_size=32),
                    steps_per_epoch=len(X_train) / 32, epochs=epochs)

# Final evaluation of the model
scores = classifier.evaluate(X_test, y_test, verbose=1)
print("Accuracy: %.2f%%" % (scores[1]*100))

# =============================================================================
#DEEP CNN "Model"
# Convolutional input layer, 32 feature maps with a size of 3×3 and a rectifier activation function
#Dropout layer at 20%
#Convolutional layer, 32 feature maps with a size of 3×3 and a rectifier activation function
#Max Pool layer with size 2×2
#Convolutional layer, 64 feature maps with a size of 3×3 and a rectifier activation function
#Dropout layer at 50%
#Convolutional layer, 64 feature maps with a size of 3×3 and a rectifier activation function
#Max Pool layer with size 2×2
#Convolutional layer, 128 feature maps with a size of 3×3 and a rectifier activation function
#Dropout layer at 50%
#Convolutional layer,128 feature maps with a size of 3×3 and a rectifier activation function
#Max Pool layer with size 2×2
#Flatten layer
#Dropout layer at 50%
#Fully connected layer with 1024 units and a rectifier activation function
#Dropout layer at 50%
#Fully connected layer with 512 units and a rectifier activation function
#Dropout layer at 50%
#Fully connected output layer with 10 units and a softmax activation function
# =============================================================================
# Create the model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), activation='relu', padding='same'))
model.add(Dropout(0.2))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Dropout(0.5))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Dropout(0.5))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dropout(0.5))
model.add(Dense(1024, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.5))
model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
# Compile model
epochs = 25
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

#larger batch size of 64
np.random.seed(seed)
#run
model.fit_generator(datagen.flow(X_train, y_train, batch_size=64),
                   steps_per_epoch=len(X_train) / 32, epochs=epochs)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))