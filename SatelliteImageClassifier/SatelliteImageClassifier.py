from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense
from keras import backend as K
from keras.callbacks import TensorBoard
import time

img_width = 50
img_height = 50

training_samples = 5725
validation_samples = 800
epoch_size = [20]

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

dense_layers = [2, 3, 4]
layer_sizes = [64, 128, 252]
conv_layers = [1, 2, 3]
batch_sizes = [8, 16]
kernal_sizes = [5, 6, 7]

for kernal_size in kernal_sizes:
    for epochs in epoch_size:
        for batch_size in batch_sizes:
            for dense_layer in dense_layers:
                for layer_size in layer_sizes:
                    for conv_layer in conv_layers:
                        model_name = "{}-conv-{}-nodes-{}-dense-{}-batch-{}-kernal-CNN-Satellite{}".format(conv_layer, layer_size,
                                                                                                  dense_layer, batch_size, kernal_size,
                                                                                                 int(time.time()))
                        tensorboard = TensorBoard(log_dir='logs/{}'.format(model_name))
                        print(model_name)

                        # Initialize the CNN
                        classifier = Sequential()

                        # Convolution layer
                        classifier.add(Convolution2D(layer_size, kernal_size, strides={2, 2}, input_shape=input_shape, activation='relu', padding='same'))
                        # Pooling layer
                        classifier.add(MaxPooling2D(pool_size=(2, 2)))

                        for l in range(conv_layer - 1):
                            # Convolution layer
                            classifier.add(Convolution2D(layer_size, 3, strides={2, 2}, activation='relu', padding='same'))
                            # Pooling layer
                            classifier.add(MaxPooling2D(pool_size=(2, 2)))

                        # Flattening
                        classifier.add(Flatten())

                        # Full connection
                        # Add the dense layers
                        for l in range(dense_layer - 1):
                            classifier.add(Dense(output_dim=layer_size, activation='relu'))

                        # Output layer
                        classifier.add(Dense(output_dim=8, activation='softmax'))

                        # Compile the CNN
                        classifier.compile(optimizer='adadelta', loss='categorical_crossentropy', metrics=['accuracy'])

                        # Fitting the CNN to the images
                        from keras.preprocessing.image import ImageDataGenerator

                        # Prepare data augmentation configuration
                        data_generator = ImageDataGenerator(
                            rescale=1. / 255,
                            validation_split=0.2,
                            horizontal_flip='true',
                        )

                        # Get training data
                        training_set = data_generator.flow_from_directory(
                            'dataset/training_set',
                            target_size=(img_width, img_height),
                            batch_size=batch_size,
                            color_mode="rgb",
                            class_mode='categorical',
                            subset="training"
                        )

                        # Get the test data
                        test_set = data_generator.flow_from_directory(
                            'dataset/training_set',
                            target_size=(img_width, img_height),
                            batch_size=batch_size,
                            color_mode="rgb",
                            class_mode='categorical',
                            subset="validation"
                        )

                        # Train the network
                        from IPython.display import display
                        from PIL import Image

                        classifier.fit_generator(
                            training_set,
                            steps_per_epoch=training_samples // batch_size,
                            epochs=epochs,
                            validation_data=test_set,
                            validation_steps=validation_samples // batch_size,
                            callbacks=[tensorboard]
                        )

                        # Save out the model
                        classifier.save(model_name + ".model")
