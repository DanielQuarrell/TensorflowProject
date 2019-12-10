import numpy as np
import tensorflow
import json
from keras.preprocessing import image

CATEGORIES = ["city_building", "dense_trees", "grass", "road", "sand", "sparse_trees", "village_building", "water"]

test_image = image.load_img('1574113320_10_05.png', target_size=(64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)

classifier = tensorflow.keras.models.load_model("64x3-CNN.model")
result = classifier.predict(test_image)

highest_category = 0

for i in range(len(CATEGORIES)):
    if result[0][i] > result[0][highest_category]:
        highest_category = i

print(CATEGORIES[highest_category])
