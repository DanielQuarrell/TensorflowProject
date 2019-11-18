import requests
import shutil
import time

from PIL import Image
from PIL import ImageFile

app_key = "JNW2RQKQlGBuYLpfDzfLillpPBaVbkYR"
width = 500
height = 500
zoom = 15
longitude = 47.6062
latitude = -122.3321
image_type = "png"

image_number = int(time.time())

image_url = f"https://www.mapquestapi.com/staticmap/v4/getmap?key={app_key}&scalebar=false&size={width},{height+50}&zoom={zoom}&center={longitude},{latitude}&type=sat&imagetype={image_type}"

response = requests.get(image_url, stream=True)
# Open the url image, set stream to True, this will return the stream content.
resp = requests.get(image_url, stream=True)
# Open a local file with wb ( write binary ) permission.
local_file = open(f"{image_number}.png", 'wb')
# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
resp.raw.decode_content = True
# Copy the response stream raw data to local image file.
shutil.copyfileobj(resp.raw, local_file)

# Remove the image url response object.
del resp

ImageFile.LOAD_TRUNCATED_IMAGES = True
img = Image.open(f"{image_number}.png")
area = (0, 0, width, height)
cropped_img = img.crop(area)
cropped_img.save(f"{image_number}.png")
