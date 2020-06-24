#!/usr/bin/env python

# draw timestamp on each .JPG in this folder
import os, time
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS


def get_exif(fn):
    """returns all EXIF data as dictionary"""
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    except:
        pass
    return ret


def get_datetime(fn):
    """returns string of year, month, day, hour, minute and second"""
    try:
        raw = get_exif(fn)["DateTime"]
    except:
        raw = "??????????????????????"
    date = {
        "year": raw[0:4],
        "month": raw[5:7],
        "day": raw[8:10],
        "hour": raw[11:13],
        "minute": raw[14:16],
        "second": raw[17:19],
    }
    datetime = (
        str(date["day"])
        + "-"
        + str(date["month"])
        + "-"
        + str(date["year"])
        + " "
        + str(date["hour"])
        + ":"
        + str(date["minute"])
    )  # format timestamp
    return datetime


maindir = os.getcwd()  # current working dir
fileList = os.listdir(maindir)  # list of files in current dir
fileList = [os.path.normcase(f) for f in fileList]  # normal case
# keep only files ending with .jpg
fileList = [f for f in fileList if ".jpg" in os.path.splitext(f)[1]]

try:
    print("First Image")
    i = Image.open(fileList[0])
    imgwidth = i.size[0]  # get width of first image
    imgheight = i.size[1]
except:
    pass

fontPath = "C:\\WINDOWS\\Fonts\\LUCON.TTF"  # font file path
myfont = ImageFont.truetype(fontPath, imgwidth // 40)  # load font and size
(textw, texth) = myfont.getsize("00-00-0000 00:00")  # get size of timestamp
x = imgwidth - textw - 50  # position of text
y = imgheight - texth - 50

print(
    "Now creating",
    str(len(fileList)),
    "frames in folder",
    time.strftime('"Frames_%Y%m%d_%H%M%S".', time.localtime()),
)

# make new dir
newdir = maindir + "\\" + time.strftime("Frames_%Y%m%d_%H%M%S", time.localtime())
os.mkdir(newdir)

for n in range(0, len(fileList)):
    i = Image.open(fileList[n])  # open image from list
    draw = ImageDraw.Draw(i)
    # thin border
    draw.text((x - 1, y - 1), get_datetime(fileList[n]), font=myfont, fill="black")
    draw.text((x + 1, y - 1), get_datetime(fileList[n]), font=myfont, fill="black")
    draw.text((x - 1, y + 1), get_datetime(fileList[n]), font=myfont, fill="black")
    draw.text((x + 1, y + 1), get_datetime(fileList[n]), font=myfont, fill="black")
    # text
    draw.text((x, y), get_datetime(fileList[n]), font=myfont, fill="white")
    os.chdir(newdir)
    i.save("Frame_" + str(n + 1) + ".jpg", quality=95)  # save in new dir
    os.chdir(maindir)
    print(str(n + 1) + ",",)

print("Done.")
time.sleep(3)
