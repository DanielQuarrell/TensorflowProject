import numpy as np
import tensorflow
import requests
import shutil
import time
import image_slicer
import os
import json

from keras.preprocessing import image
from PIL import Image
from PIL import ImageFile

CATEGORIES = ["city_building", "dense_trees", "grass", "road", "sand", "sparse_trees", "village_building", "water"]

app_key = "JNW2RQKQlGBuYLpfDzfLillpPBaVbkYR"
width = 1500
height = 1500
zoom = 17
# latitude = 52.194566
# longitude = -2.229986

# latitude = 52.627128
# longitude = -2.099064

# latitude = 50.356280
# longitude = -4.449498

# latitude = 51.379941
# longitude = 1.337326

latitude = 50.331046
longitude = -4.517390

image_type = "png"

tile_width = 50
tile_height = 50

map_width = width / tile_width
map_height = height / tile_height

image_number = int(time.time())

image_url = f"https://www.mapquestapi.com/staticmap/v4/getmap?key={app_key}&scalebar=false&size={width},{height+50}&zoom={zoom}&center={latitude},{longitude}&type=sat&imagetype={image_type}"

print("Requesting image")
response = requests.get(image_url, stream=True)
print("1")
# Open the url image, set stream to True, this will return the stream content.
resp = requests.get(image_url, stream=True)
print("2")
# Open a local file with wb (write binary) permission.
local_file = open(f"TestSatelliteImage/Original/{image_number}.png", 'wb')
print("3")
# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
resp.raw.decode_content = True
print("4")
# Copy the response stream raw data to local image file.
shutil.copyfileobj(resp.raw, local_file)
print("5")
# Remove the image url response object.
del resp

print("Cropping image")
# Crop the image to remove the watermark provided by the API
ImageFile.LOAD_TRUNCATED_IMAGES = True
img = Image.open(f"TestSatelliteImage/Original/{image_number}.png")
area = (0, 0, width, height)
cropped_img = img.crop(area)
cropped_img.save(f"TestSatelliteImage/Original/{image_number}.png")

print("Splitting image")
# Slice the image into 100 even chunks from a 50 x 50 image
tiled_image = image_slicer.slice(f"TestSatelliteImage/Original/{image_number}.png", (width * height) / (tile_width * tile_height), save=False)
image_slicer.save_tiles(tiled_image, directory="TestSatelliteImage/Sliced")

# Best 2-conv-64-nodes-2-dense-8-batch-CNN-Satellite1577977211 <-----
# 2-conv-64-nodes-0-dense-8-batch-CNN-Satellite1577979525.model
# 2-conv-128-nodes-1-dense-8-batch-CNN-Satellite1577981776.model

classifier = tensorflow.keras.models.load_model("2-conv-64-nodes-2-dense-8-batch-CNN-Satellite1577977211.model")

image_dir = "TestSatelliteImage/Sliced/"

map_data = []

print("Analysing segments")
# Loop through each image
for image_path in os.listdir(image_dir):

    # Open Image
    test_image = image.load_img(f"TestSatelliteImage/Sliced/{image_path}", target_size=(tile_width, tile_height))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    # Classify image
    result = classifier.predict(test_image)

    # Output result to json
    highest_category = 0

    for i in range(len(CATEGORIES)):
        if result[0][i] > result[0][highest_category]:
            highest_category = i

    print(result[0])
    map_data.append(CATEGORIES[highest_category])

json_object = {
    'width' : map_width,
    'height' : map_height,
    'map_data' : map_data
}

with open('map_data.json', 'w') as json_file:
    json.dump(json_object, json_file)
