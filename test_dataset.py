import cv2
import xlwrite
import time
import sys
import base64
import numpy as np

class TestData:
    def __init__(self):
        self.period = 30
        self.face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer.yml')
        self.filename = 'filename'
        self.attendance = {'item1': 1}
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.count = 0

    def test(self, input_str):
        flag = 0
        img = cv2.imdecode(np.frombuffer(base64.b64decode(input_str), dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cas.detectMultiScale(gray, 1.3, 7)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
            id, conf = self.recognizer.predict(roi_gray)
            print(id, conf)
            if conf < 105:
                if id == 1:
                    id='Souvik Ghosh'
                    if str(id) not in self.attendance:
                        self.filename = xlwrite.output('attendance', 'class1', 1, id, 'yes')
                        self.attendance[str(id)] = str(id)
                elif id == 2:
                    id = 'Indranil Das'
                    if str(id) not in self.attendance:
                        self.filename = xlwrite.output('attendance', 'class1', 2, id, 'yes')
                        self.attendance[str(id)] = str(id)
                elif id  == 3:
                    id = 'Kingshuk Mukherjee'
                    if str(id) not in self.attendance:
                        self.filename = xlwrite.output('attendance', 'class1', 3, id, 'yes')
                        self.attendance[str(id)] = str(id)
                elif id == 4:
                    id = 'Ki'
                    if str(id) not in self.attendance:
                        self.filename = xlwrite.output('attendance', 'class1', 4, id, 'yes')
                        self.attendance[str(id)] = str(id)
            else:
                id = 'Unknown, can not recognize'
                flag = flag + 1
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Spoof Detected", (x, y-10), self.font, 0.55, (120, 255, 120), 1)
                break

            cv2.putText(img, str(id), (x, y-10), self.font, 0.55, (120, 255, 120), 1)
            self.count = self.count + 1

        _, im_arr = cv2.imencode('.jpg', img)
        if self.count > 30:
            self.count = 0
            return (base64.b64encode(im_arr.tobytes()).decode("utf-8"), True)
        return (base64.b64encode(im_arr.tobytes()).decode("utf-8"), False)