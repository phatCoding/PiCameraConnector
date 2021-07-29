import cv2 
import mediapipe as mp

class HandDetector:

    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def show(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.hands.process(imgRGB)

        if res.multi_hand_landmarks:
            for handLms in res.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
