from time import sleep
from io import BytesIO
from picamera import PiCamera
import numpy as np
import json
import os

width = 320
height = 240
size = width * height
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
print('config path: {}'.format(config_path))
targets = np.loadtxt(config_path, dtype=int)
ratio = 8
thres = 3000


def main():
    if len(targets) == 0:
        print('invalid config file')
        return
    # Create an in-memory stream
    camera = PiCamera()
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    last_data = None
    while True:
        my_stream = BytesIO()
        camera.capture(my_stream, format='yuv', resize=(width, height))
        data = bytearray(size)
        ret = my_stream.readinto(data)
        my_stream.close()
        if ret != size:
            print("read from stream failed, ret: {}".format(ret))

        if last_data is not None:
            judge_motion(last_data, data)
        judge_light(data)

        last_data = data
        try:
            sleep(0.5)
        except KeyboardInterrupt:
            break
    print("main loop finished")


def judge_light(current):
    if len(current) != size:
        print('invalid input for judge light')
        return
    pass


def judge_motion(last, current):
    if len(last) != size or len(current) != size:
        print('invalid input for judge motion')
        return

    rects = np.divide(targets, ratio).astype(int)
    inner_width = int(width / ratio)
    inner_height = int(height / ratio)
    # 差值
    diff = np.zeros((inner_width, inner_height))
    for i in range(inner_width):
        for j in range(inner_height):
            ic = current[i * ratio: (i + 1) * ratio]
            il = last[i * ratio: (i + 1) * ratio]
            idiff = np.subtract(ic, il)
            diff[i, j] = np.sum(idiff)
    # 二值化
    diff[diff >= thres] = 1
    diff[diff < thres] = 0
    print(diff)

    res = []
    for i in range(len(rects)):
        rect = rects[i]
        submatrix = diff[rect[0]:rect[2], rect[1]:rect[3]]
        print(submatrix)
        if np.sum(submatrix) > 0:
            res.append(i)

    if len(res) > 0:
        with open('/home/pi/motion/fifo', 'w', encoding='utf-8') as file:
            file.write(json.dumps({'motion': res}))


if __name__ == '__main__':
    main()
    # judge_motion(np.ones(size), np.zeros(size))

