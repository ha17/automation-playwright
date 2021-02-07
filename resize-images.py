# From: https://sempioneer.com/python-for-seo/image-resizing-in-python/

from PIL import Image
import PIL
import os
import glob

directory_files = os.listdir()
multiple_images = [file for file in directory_files if file.endswith(('.jpg', '.png'))]
print(multiple_images)

for image in multiple_images:
    img = Image.open(image)
    img.thumbnail(size=(300,300))
    print(img)

#multiple_images = [file for file in directory_files if 'example' in file and file.endswith(('.jpg', '.png'))]