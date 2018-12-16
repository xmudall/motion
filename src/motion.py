import time
from picamera import PiCamera
import numpy as np
import json
import os
from flask import Flask, render_template, request, jsonify
import threading

width = 64 * 2
height = 48 * 2
ratio = 8
sthres = 1
thres = ratio * ratio * 255 / 30
size = width * height
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/ss.jpg')
print('config path: {}, image path: {}'.format(config_path, image_path))
targets = np.loadtxt(config_path, dtype=int)
rects = np.divide(targets, ratio * 320 / width).astype(int)
snapping = False

# camera
camera = PiCamera()
camera.start_preview()
# Camera warm-up time
time.sleep(2)

# flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/snap')
def post_snap():
    snap()
    return ''


@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        set_config(request.json)
        return ''
    else:
        return get_config()


def set_config(config):
    if len(config) == 0:
        return
    with open(config_path, 'w', encoding='utf-8') as file:
        for line in config:
            file.write(' '.join(str(x) for x in line) + '\n')
    global targets
    targets = np.loadtxt(config_path, dtype=int)


def get_config():
    return jsonify(targets.tolist())


def start_app():
    # run app
    app.run(host='0.0.0.0')


def main():
    t = threading.Thread(name='web', target=start_app)
    t.daemon = True
    t.start()

    # Create an in-memory stream
    last_data = None
    # count = 0
    while True:
        if snapping:
            time.sleep(1)
            continue
        data = np.empty((width, height), dtype=np.uint8)
        try:
            camera.capture(data, format='yuv', resize=(width, height))
        except IOError as e:
            pass
        # for i in range(height):
        #     print(' '.join('{:3d}'.format(x) for x in data[i * width: (i+1) * width]))
        # print('\n\n')

        if last_data is not None:
            judge_motion(last_data, data)
        judge_light(data)
        last_data = data

        # count = count + 1
        # if count % 10 == 0:
        #     snap()

        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
    print("main loop finished")


def snap():
    global snapping
    snapping = True
    time.sleep(2)
    with open(image_path, 'wb+') as file:
        camera.capture(file, resize=(320, 240))
    snapping = False


def judge_light(current):

    res = {}
    for i in range(len(rects)):
        rect = rects[i]
        submatrix = current[rect[0]:rect[2], rect[1]:rect[3]]
        res[i] = int(np.average(submatrix))

    with open('/home/pi/motion/fifo', 'w', encoding='utf-8') as file:
        out = json.dumps({'light': res}) + '\n'
        print('write to serial: {}'.format(out))
        file.write(out)


def judge_motion(last, current):
    # if len(last) != size or len(current) != size:
    #     print('invalid input for judge motion')
    #     return
    start = time.clock()

    # 差值
    ih = int(height / ratio)
    iw = int(width / ratio)
    idiff = np.abs(np.subtract(last.astype(int), current.astype(int)))
    idiff[idiff < sthres] = 0
    diff = np.sum(idiff.reshape(ih, ratio, iw, -1), axis=(1,3))
    # 二值化
    # print(diff)
    diff[diff < thres] = 0
    diff[diff >= thres] = 1
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
            out = json.dumps({'motion': res}) + '\n'
            print('write to serial: {}'.format(out))
            file.write(out)

    print('judge motion used: {}'.format(time.clock() - start))


if __name__ == '__main__':
    main()
    # judge_motion(np.ones(size), np.zeros(size))
