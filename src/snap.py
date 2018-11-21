from time import sleep
from picamera import PiCamera
import os

image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web/static/ss.jpg')
print('config path: {}'.format(image_path))

camera = PiCamera()
camera.start_preview()
sleep(2)
for filename in camera.capture_continuous(image_path):
    print('Captured %s' % filename)
    sleep(5) # wait 5 minutes