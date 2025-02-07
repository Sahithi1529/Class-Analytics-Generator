# All Camera related Code Here
import cv2 as cv
from Class_Analytics_Generator import settings
import os
import torch
from torchvision import transforms
class Camera():
    def __init__(self):
        '''
        Constructor which creates Cam object
        '''
        self.cam = cv.VideoCapture(0) # cam object
        self.face_detector = cv.CascadeClassifier(os.path.join(settings.BASE_DIR,'static','resources','haarcascade_frontalface_default.xml'))
    def getFrame(self):
        '''
        Capture a Picture and return grayimage of picture to send for model
        returns None if image is not read
        '''
        ret,frame = self.cam.read()
        if ret:
            gray_image = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) # Converting Image into Frame
            return gray_image
        else:
            print("Unable to Capture frame")
            return None
    def resizeFrame(self,frame,dimensions):
        '''
        Accepts a frame and resize it to specified dimensions
        dimensions is a tuple (x,y) indicating new dimensions
        '''
        return cv.resize(frame,dimensions)
    def detectFaces(self,frame):
        self.faces = self.face_detector.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=3)
        self.faces = self.face_detector.detectMultiScale(frame,1.1,3)
        self.final_faces = []
        for (x,y,w,h) in self.faces:
         self.final_faces.append(frame[y:y+h,x:x+w])
        return self.final_faces
    
class Model():
    def __init__(self):
        self.model = torch.load(os.path.join(settings.BASE_DIR,'static','resources','model.pt'),weights_only=False,map_location=torch.device('cpu'))
        # self.model
    
    def preprocess(self,frame):
        transformations = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5),(0.5))
            ]
        )
        frame = transformations(frame)
        return frame
    
    def predict(self,frame):
        # self.model.eval()
        # outputs = self.model(frame)
        # print(outputs)
        prediction = {
            'Bored':[2],
            'Confused':[3],
            'Focused':[4],
            'Sleepy':[1],
            'Engaged':[7],
            'Not Engaged':[3],
            'total': [10]
        }
        return prediction
    