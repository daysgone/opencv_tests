import picamera
from time import sleep

camera = picamera.PiCamera()
camera.start_preview()

for i in range(100):
    camera.brightness = i
    sleep(0.2)