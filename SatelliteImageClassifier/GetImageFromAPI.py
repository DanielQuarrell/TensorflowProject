import requests
import shutil
import time
import image_slicer

from PIL import Image
from PIL import ImageFile

app_key = "JNW2RQKQlGBuYLpfDzfLillpPBaVbkYR"
width = 500
height = 500
zoom = 17
longitude = 51.511375
latitude = -2.543449
image_type = "png"

image_number = int(time.time())

image_url = f"https://www.mapquestapi.com/staticmap/v4/getmap?key={app_key}&scalebar=false&size={width},{height+50}&zoom={zoom}&center={longitude},{latitude}&type=sat&imagetype={image_type}"

response = requests.get(image_url, stream=True)
# Open the url image, set stream to True, this will return the stream content.
resp = requests.get(image_url, stream=True)
# Open a local file with wb ( write binary ) permission.
local_file = open(f"TrainingData/{image_number}.png", 'wb')
# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
resp.raw.decode_content = True
# Copy the response stream raw data to local image file.
shutil.copyfileobj(resp.raw, local_file)

# Remove the image url response object.
del resp

# Crop the image to remove the watermark provided by the API
ImageFile.LOAD_TRUNCATED_IMAGES = True
img = Image.open(f"TrainingData/{image_number}.png")
area = (0, 0, width, height)
cropped_img = img.crop(area)
cropped_img.save(f"TrainingData/{image_number}.png")

# Slice the image into 100 even chunks from a 50 x 50 image
image_slicer.slice(f"TrainingData/{image_number}.png", 100)



