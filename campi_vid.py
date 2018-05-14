''' WrightRocket Videocam for Raspberry Pi
    By Keith Wright
    Created May 14, 2018
'''
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.start_recording('/home/pi/video.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview()
