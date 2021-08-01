import cv2 , socket
import numpy as np
import base64
import mediapipe as mp

from flask import Flask, render_template, Response
app = Flask(__name__)

BUFF_SIZE = 65536
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

if __name__ == "__main__":
    app.run(debug=True)


def gen_frames():
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

            #cv2.imshow("recv video", frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        
            key = cv2.waitKey(1) & 0xFF

        except Exception as err:
            print(err)
            clientSock.close()
            cv2.destroyAllWindows()
            break

        if key == 27:
            clientSock.close()
            cv2.destroyAllWindows()
            break

#######
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')