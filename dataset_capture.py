import cv2
import os
import numpy as np
import base64
import pickle

class DatasetCapture:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.count = 0
        self.data = []
        try:
            predata = pickle.loads(open("data.pickle", "rb").read())
        except:
            predata = dict()
            with open("data.pickle", "wb") as f:
                f.write(pickle.dumps(predata))

    def capture(self, id, input_str):
        header, encoded = input_str.split(",", 1)
        frame = cv2.imdecode(np.frombuffer(base64.b64decode(encoded), dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            self.count += 1
            image = dict()
            image[str(str(id) + '.' + str(self.count))] = gray[y:y+h, x:x+w]
            self.data.append(image)
        if self.count > 15:
            self.count = 0
            data = pickle.loads(open("data.pickle", "rb").read())
            data[id] = self.data
            with open("data.pickle", "wb") as f:
                f.write(pickle.dumps(data))
            self.data = []
            return False
        return True