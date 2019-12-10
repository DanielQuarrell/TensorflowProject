from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense
from keras import backend as K
from keras.callbacks import TensorBoard

img_width = 50
img_height = 50

training_samples = 4000
validation_samples = 800
epochs = 75
batch_size = 16

model_name = "64x3-CNN-Satellite"
tensorboard = TensorBoard(log_dir='logs/{}'.format(model_name))

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

# Part 1 - Initialize the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Convolution2D(32, 5, 5, input_shape=input_shape, activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step 3 - Flatting
classifier.add(Flatten())
# Step 4 - Full Connection
classifier.add(Dense(output_dim=64, activation='relu'))

classifier.add(Dense(output_dim=8, activation='softmax'))

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Part 5 - Fitting the CNN to the images
from keras.preprocessing.image import ImageDataGenerator

# prepare data augmentation configuration
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    horizontal_flip=True,
    vertical_flip=True,
)

test_datagen = ImageDataGenerator(rescale=1/.255)

training_set = train_datagen.flow_from_directory(
    'dataset/training_set',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

test_set = test_datagen.flow_from_directory(
    'dataset/test_set',
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

# Part 6 - Training the network
from IPython.display import display
from PIL import Image

classifier.fit_generator(
    training_set,
    steps_per_epoch=training_samples // batch_size,
    epochs=epochs,
    validation_data=test_set,
    validation_steps=validation_samples // batch_size,
    class_weight='auto',
    callbacks=[tensorboard]
)

# Part 7 - Save the model
classifier.save(model_name + ".model")
