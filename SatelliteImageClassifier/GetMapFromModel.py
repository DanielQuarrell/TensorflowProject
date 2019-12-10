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
longitude = 51.879207
latitude = -1.315504
image_type = "png"

tile_width = 50
tile_height = 50

map_width = width / tile_width
map_height = height / tile_height

image_number = int(time.time())

image_url = f"https://www.mapquestapi.com/staticmap/v4/getmap?key={app_key}&scalebar=false&size={width},{height+50}&zoom={zoom}&center={longitude},{latitude}&type=sat&imagetype={image_type}"

response = requests.get(image_url, stream=True)
# Open the url image, set stream to True, this will return the stream content.
resp = requests.get(image_url, stream=True)
# Open a local file with wb ( write binary ) permission.
local_file = open(f"TestSatelliteImage/Original/{image_number}.png", 'wb')
# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
resp.raw.decode_content = True
# Copy the response stream raw data to local image file.
shutil.copyfileobj(resp.raw, local_file)

# Remove the image url response object.
del resp

# Crop the image to remove the watermark provided by the API
ImageFile.LOAD_TRUNCATED_IMAGES = True
img = Image.open(f"TestSatelliteImage/Original/{image_number}.png")
area = (0, 0, width, height)
cropped_img = img.crop(area)
cropped_img.save(f"TestSatelliteImage/Original/{image_number}.png")

# Slice the image into 100 even chunks from a 50 x 50 image
tiled_image = image_slicer.slice(f"TestSatelliteImage/Original/{image_number}.png", (width * height) / (tile_width * tile_height), save=False)
image_slicer.save_tiles(tiled_image, directory="TestSatelliteImage/Sliced")

classifier = tensorflow.keras.models.load_model("64x3-CNN-Satellite.model")

image_dir = "TestSatelliteImage/Sliced/"

map_data = []

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