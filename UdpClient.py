import cv2 , socket
import numpy as np
import base64

import mediapipe as mp

BUFF_SIZE = 16384 
UDP_IP_ADDRESS = '192.168.178.171'
UDP_PORT_NO = 6789

msg = "Desk".encode()
bytearray = bytearray(msg)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
clientSock.sendto(bytearray, (UDP_IP_ADDRESS, UDP_PORT_NO))

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:

    try:
        packet,_ = clientSock.recvfrom(BUFF_SIZE)
        data = base64.b64decode(packet, ' /')
        npdata = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(imgRGB)

        if res.multi_hand_landmarks:
            for handLms in res.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, handLms,mpHands.HAND_CONNECTIONS)

        cv2.imshow("recv video", frame)
        key = cv2.waitKey(1) & 0xFF

    except:
        clientSock.close()
        cv2.destroyAllWindows()
        break

    if key == 27:
        clientSock.close()
        cv2.destroyAllWindows()
        break
