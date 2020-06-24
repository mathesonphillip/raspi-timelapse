#!/usr/bin/env python

from PIL import Image, ExifTags

img = Image.open("./raw-frames/001.jpg")
print(dir(img))
# [... 'getexif' ...]

img_exif = img.getexif()
if img_exif:
    print(type(img_exif))
    # <class 'PIL.Image.Exif'>
    print(dict(img_exif))
    # { .. 271: 'FUJIFILM', 305: 'Adobe Photoshop Lightroom 6.14 (Macintosh)', }

    img_exif_dict = dict(img_exif)
    for key, val in img_exif_dict.items():
        if key in ExifTags.TAGS:
            print(ExifTags.TAGS[key] + " - " + str(val))
else:
    print("Sorry, image has no exif data.")
