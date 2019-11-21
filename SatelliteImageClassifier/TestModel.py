import numpy as np
import tensorflow
from keras.preprocessing import image

test_image = image.load_img('1574113320_08_02.png', target_size=(64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)

classifier = tensorflow.keras.models.load_model("64x3-CNN.model")
result = classifier.predict(test_image)

print(result)
