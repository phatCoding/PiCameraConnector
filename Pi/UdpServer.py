from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import socket
import cv2
import base64
import numpy as np
import sys

VID_RESOLUTION = (640,480)
BUFFER = 65536
UDP_IP = '192.168.178.171'
UDP_PORT = 6789
VID_WIDTH = 400

camera = PiCamera()
camera.resolution = VID_RESOLUTION
camera.framerate = 24
time.sleep(2)
rawCapture = PiRGBArray(camera, size=VID_RESOLUTION)

ServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER)
ServerSock.bind((UDP_IP,UDP_PORT))
while True:
    try:
        print("Est Connection")
        _, client = ServerSock.recvfrom(BUFFER)

        for frame in camera.capture_continuos(rawCapture, format="bgr", use_video_port= True):

            try:
                frame = cv2.resize(frame.array, (400,370))
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY,80])
                message = base64.b64encode(buffer)
                ServerSock.sendto(message, client)
                rawCapture.truncate(0)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:
                    camera.close()
                    ServerSock.close()
                    break

            except Exception as err:
                print(err)
                camera.close()
                sys.exit(1)
    except:
        camera.close()
        ServerSock.close()
        break