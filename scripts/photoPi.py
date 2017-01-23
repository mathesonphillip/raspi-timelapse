#script to install to pi?
#instructions
#config file that can be updated via web page and paste over
#website to hold custom config file and original config file
#make changes on web site and save.
#Download script on pi

import config
import random
import string
import datetime
import os
from time import sleep
from picamera import PiCamera

#Seconds


def main():
    #Generate random string to append to folder name
    randString = rand_string();
    #Generate string with todays date
    today = datetime.date.today().strftime('%Y%m%d');
    #Combine date and random string as directory name 
    directory = config.PATH_TO_PHOTOS + today + '-' + randString
    #Create directory
    os.makedirs(directory)

    #Initialise Camera
    camera = PiCamera()
    setCameraSettings(camera)
    #Camera warm-up time
    sleep(2)
    
    for filename in camera.capture_continuous(directory + "/image_{counter:04d}.jpg"):
        sleep(config.PHOTO_INTERVAL) # wait 5 minutes

#Function used to generate random string for folder name
def rand_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def setCameraSettings(camera):
    camera.resolution = config.RESOLUTION
    camera.rotation = config.ROTATION
    camera.exif_tags['EXIF.UserComment'] = config.USER_COMMENT
    camera.iso = config.ISO

#Run the main function
main()