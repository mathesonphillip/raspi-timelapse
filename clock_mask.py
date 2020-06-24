#!/usr/bin/env python

# draw clock (with marks) as mask on images in folder
import os, time, numpy, aggdraw
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from PIL.ExifTags import TAGS


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()


def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val

    return labeled


def clock(i, x, y, radius, color, opacity, date):
    """draws a clock on image i, returns image i"""

    # calculate pointer angles
    sec = -2 * numpy.pi * int(date["second"]) / 60 + numpy.pi / 2
    mnt = (
        -2 * numpy.pi * (int(date["minute"]) + int(date["second"]) / 60.0) / 60.0
        + numpy.pi / 2
    )
    hrs = (
        -2
        * numpy.pi
        * (
            int(date["hour"])
            + int(date["minute"]) / 60.0
            + int(date["second"]) / 3600.0
        )
        / 12.0
        + numpy.pi / 2
    )
    # 2nd pointer coordinates
    second = x + radius / 1.2 * numpy.cos(sec), y - radius / 1.2 * numpy.sin(sec)
    minute = x + radius / 1.1 * numpy.cos(mnt), y - radius / 1.1 * numpy.sin(mnt)
    hour = x + radius / 1.7 * numpy.cos(hrs), y - radius / 1.7 * numpy.sin(hrs)

    # marks angles
    marks = 12  # number of marks
    angles = [numpy.pi / 2]  # angles of marks, beginning with top
    step = 2.0 * numpy.pi / marks  # step in angle between marks
    [angles.append(angles[-1] - step) for n in range(1, marks)]

    # marks coordinates
    mark = []  # (x1, y1, x2, y2)
    for angle in angles:
        mark.append(
            (
                x + radius / 1.25 * numpy.cos(angle),
                y - radius / 1.25 * numpy.sin(angle),
                x + radius / 1.0 * numpy.cos(angle),
                y - radius / 1.0 * numpy.sin(angle),
            )
        )

    # draw clock
    draw = aggdraw.Draw(i)  # draw on image i
    p = aggdraw.Pen(color, width=radius / 15.0, opacity=opacity)  # create pen
    draw.line([x, y, hour[0], hour[1]], p)  # draw line
    p = aggdraw.Pen(color, width=radius / 25.0, opacity=opacity)
    draw.line([x, y, minute[0], minute[1]], p)
    # p = aggdraw.Pen(color, width=radius / 50., opacity=opacity) # optional seconds pointer
    # draw.line([x, y, second[0], second[1]], p)
    # p = aggdraw.Pen(color, width=radius/25, opacity=opacity) # optional ring
    # draw.ellipse([x-radius, y-radius, x+radius, y+radius], p)
    p = aggdraw.Pen(color, width=radius / 20.0, opacity=opacity)
    for tup in mark:
        draw.line([tup[0], tup[1], tup[2], tup[3]], p)
    b = aggdraw.Brush(color, opacity)
    draw.ellipse(
        [x - radius / 30, y - radius / 30, x + radius / 30, y + radius / 30], b
    )
    draw.flush()  # draw!
    return i


def main():

    maindir = os.getcwd()  # current working dir

    # make list of .jpg files in dir
    fileList = os.listdir(maindir)  # create list of all files in current dir
    fileList = [os.path.normcase(f) for f in fileList]  # normal case extension
    fileList = [
        f for f in fileList if ".jpg" in os.path.splitext(f)[1]
    ]  # keep .jpg files only

    # make new subfolder where new images will be placed
    dirname = time.strftime("Frames_%Y%m%d_%H%M%S", time.localtime())
    newdir = maindir + "\\" + dirname
    os.mkdir(newdir)

    # calculate radius and position of clock based on image width
    try:
        i = Image.open(fileList[0])
        imgwidth = i.size[0]  # get width of first image
        imgheight = i.size[1]
    except:
        pass

    r = imgwidth / 15  # clock radius
    x = imgwidth - r * 1.5  # clock position
    y = imgheight - r * 1.5
    color = "white"
    opacity = 255

    print("Now creating", str(len(fileList)), "frames in folder", dirname)

    for n in range(0, len(fileList)):
        # open image n
        image = Image.open(fileList[n])
        # make copy of image and alter it: Brightness, Contrast, Sharpness
        i2 = ImageEnhance.Brightness(image)
        i2 = i2.enhance(2.0)  # enhance factor

        # get EXIF tags
        ret = {}
        info = image._getexif()

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        print(ret)

        # get date and time from EXIF tag
        try:
            raw = ret["DateTime"]
        except:
            raw = "00000000000000000000"
        date = {
            "year": raw[0:4],
            "month": raw[5:7],
            "day": raw[8:10],
            "hour": raw[11:13],
            "minute": raw[14:16],
            "second": raw[17:19],
        }

        mask = Image.new(
            "RGB", (imgwidth, imgheight), "black"
        )  # create PIL image (mask)
        # draw clock on mask
        print(date)
        mask = clock(mask, x, y, r, color, opacity, date)  # draw clock on mask
        mask = mask.convert("L")  # mask needs to be 'L' for some reason to composite

        # composite images
        i = Image.composite(i2, image, mask)

        # save image in the new subfolder
        os.chdir(newdir)
        i.save("Frame_" + str(n + 1) + ".jpg", quality=95)  # save in new dir
        os.chdir(maindir)  # back to main folder
        print(str(n + 1) + ",",)

    print("done.")
    time.sleep(3)


if __name__ == "__main__":
    main()
    # img = Image.open("./00000050.jpg")
    # exif = {
    #     ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS
    # }
    # print(exif)

    # exif = get_exif
    # print(exif)
    # labeled = get_labeled_exif(exif)
    # print(labeled)
