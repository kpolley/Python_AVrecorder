import io
import sys
import math
from pathlib import Path

import picamera
from PIL import Image
from PIL import ImageStat

from p_iris_ctrl import p_iris_ctrl

home = str(Path.home())

iso_options = [100, 200, 320, 400, 500, 640, 800]
speed_options = [500, 1000, 2000, 4000, 8000, 16667, 33333]

# Starting values of iso and speed:
iso = 1
speed = 3
iris = 0

# Exposure control constants:
TARGET_XP = 120
TOLERANCE = 5
GAIN = 0.1

camera = picamera.PiCamera()


def aperture(value):
    p_iris_ctrl(target_aperture=int(value))


def write_to_file(filename, content):
    while True:
        try:
            f = open(filename, "w")
            f.write(content)
            f.close()
        except:
            continue
        break


def brightness(preview_image):
    try:
        im = preview_image.convert('L')
        stat = ImageStat.Stat(im)
        return stat.mean[0]
    except:
        print("Error calculating brightness from image")
        exit()


def saturate(value, minimum, maximum):
    if value > maximum:
        return maximum
    if value < minimum:
        return minimum
    return value


def capture_preview():
    global camera, iso, iso_options, speed, speed_options
    camera.start_preview()
    stream = io.BytesIO()
    camera.iso = iso_options[iso]
    camera.shutter_speed = speed_options[speed]
    camera.zoom = (0, 0, 1, 1)  # (x, y, w, h)
    camera.capture(stream, format='jpeg', resize=(320, 240))
    stream.seek(0)
    image = Image.open(stream)
    return image


try:
    if len(sys.argv) - 1 > 1:
        print("Too many arguments!")
        exit()

    if len(sys.argv) - 1 == 1:
        TARGET_XP = sys.argv[1]
    if not str(TARGET_XP).isdecimal():
        print("Target must be a number between 0 and 255")
        exit()
    TARGET_XP = int(TARGET_XP)
    TARGET_XP = saturate(TARGET_XP, 0, 255)

    camera.start_preview()
    ready = False
    while not ready:
        print("Testing iso " + str(iso_options[iso]) + ", speed " + str(speed_options[speed]) + ", aperture " + str(iris))
        aperture(iris)
        exposure_error = TARGET_XP - brightness(capture_preview())

        if exposure_error > TOLERANCE:
            if iris > 0:
                iris = saturate(iris - math.ceil(exposure_error * GAIN), 0, 100)
            elif speed < len(speed_options) - 1:
                speed += 1
            elif iso < len(iso_options) - 1:
                iso += 1
            else:
                print("Environment too dark! Unable to expose image to target of " + str(TARGET_XP))
                exit()

        elif exposure_error < -TOLERANCE:
            if iris < 100:
                iris = saturate(iris + math.ceil(-exposure_error * GAIN), 0, 100)
            elif speed > 0:
                speed -= 1
            elif iso > 0:
                iso -= 1
            else:
                print("Environment too bright! unable to expose image to target of " + str(TARGET_XP))

        else:
            ready = True

    print("Settings successful! Writing to camera_settings.txt")
    write_to_file(home + "/aa-cam/camera_settings.txt", str(iso_options[iso]) + "\n" + str(speed_options[speed]) + "\n")

finally:
    camera.stop_preview()
    camera.close()
