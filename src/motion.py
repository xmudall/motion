from time import sleep
from io import BytesIO
from picamera import PiCamera
import numpy as np

size = 76800


def main():
    # Create an in-memory stream
    camera = PiCamera()
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    last_data = None
    while True:
        my_stream = BytesIO()
        camera.capture(my_stream, format='yuv', resize=(320, 240))
        data = bytearray(size)
        ret = my_stream.readinto(data)
        my_stream.close()
        if ret != size:
            print "read from stream failed, ret: {}".format(ret)

        if last_data is not None:
            judge_motion(last_data, data)
        judge_light(data)

        last_data = data
        try:
            sleep(0.5)
        except KeyboardInterrupt:
            break
    print "main loop finished"


def judge_light(current):
    pass


def judge_motion(last, current):
    ratio = 4
    diff = np.array('i')
    for i in range(size / ratio / ratio):
        n = 0
        for j in range(ratio):
            pass
        diff.append()
    pass


if __name__ == '__main__':
    main()

