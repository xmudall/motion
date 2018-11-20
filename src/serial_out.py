import queue
import serial
import threading
import time
import json


def main():
    # s = serial.Serial('/dev/ttyAMA0', 115200)
    s = serial.Serial('/dev/tty.usbserial-1420', 115200)
    q = queue.Queue()
    t = threading.Thread(name='read fifo', target=read, args=['/tmp/fifo', q])
    t.start()
    while True:
        if q.empty():
            time.sleep(1)
            continue
        line = q.get()
        send_data(line, s)

    pass


def send_data(data, s):
    # data like { "motion": [ 1, 2, 4], "light": [2, 6] }
    print("send data: {}".format(data))
    try:
        input = json.loads(data)
    except Exception as e:
        print("can't parse data: {}".format(e))
        return
    motion = 0
    light = 0
    if "motion" in input:
        motion = build_byte(input["motion"])
    if "light" in input:
        light = build_byte(input["light"])
    out = bytes([0xfa, 0x01, motion, light, 0, 0, 0, 0, 0, 0])
    crc = crc_bytes(0x07, out)
    print(', '.join('0x{:02x}'.format(x) for x in out))
    print(hex(crc))
    s.write(out)
    s.write(crc)


def build_byte(arr):
    out = 0
    for i in range(0, len(arr)):
        out = out + (0x01 << arr[i])
    return out


def crc_bytes(poly, byte_arr):
    crc = 0
    for i in range(0, len(byte_arr)):
        crc = crc_byte(poly, crc ^ byte_arr[i])
    return crc


def crc_byte(poly, data):
    crc = data
    for bit in range(0, 8):
        if crc & 0x80:
            crc = (crc << 1) ^ poly
        else:
            crc = (crc << 1)
    return crc & 0xff


def read(filename, q):
    print('start reading from fifo')
    with open(filename, 'r', encoding='utf-8') as ifile:
        while True:
            line = ifile.readline()
            if line == '':
                time.sleep(0.01)
                continue
            if q.qsize() > 10:
                continue
            q.put(line)


if __name__ == '__main__':
    main()
    # send_data('{ "motion": [ 1, 2, 4], "light": [2, 6] }', None)
    # print(hex(crc_bytes(0x07, [0xfa, 0x01, 0x0f, 0x0f, 0, 0, 0, 0, 0, 0])))

