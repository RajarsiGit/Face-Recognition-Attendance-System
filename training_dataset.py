import cv2
import os
import numpy as np
import pickle

class TrainData:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.data = []

    def getImagesAndLabels(self, data):
        faceSamples = []
        Ids = []
        for key in data:
            for items in data[key]:
                id = list(items.keys())[0]
                faces = self.detector.detectMultiScale(items[id])
                for (x, y, w, h) in faces:
                    faceSamples.append(items[id][y:y+h, x:x+w])
                    Ids.append(int(id.split('.')[0]))
        return faceSamples, Ids
    
    def train(self):
        try:
            data = pickle.loads(open('data.pickle', "rb").read())
        except:
            return False
        faces, Ids = self.getImagesAndLabels(data)
        s = self.recognizer.train(faces, np.array(Ids))
        self.recognizer.write('trainer.yml')
        return True