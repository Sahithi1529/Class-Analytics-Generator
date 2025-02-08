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
            # return frame
        else:
            print("Unable to Capture frame")
            return None
    def resizeFrame(self,frames,dimensions):
        '''
        Accepts a frame and resize it to specified dimensions
        dimensions is a tuple (x,y) indicating new dimensions
        '''
        resized_faces = []
        for frame in frames:
            resized_faces.append(cv.resize(frame,dimensions))
        print("No of faces for resize",len(resized_faces))
        return resized_faces
    
    def detectFaces(self,frame):
        self.faces = self.face_detector.detectMultiScale(frame,scaleFactor=1.1,minNeighbors=3)
        self.faces = self.face_detector.detectMultiScale(frame,1.1,3)
        self.final_faces = []
        for (x,y,w,h) in self.faces:
         self.final_faces.append(frame[y:y+h,x:x+w])
        print("No of faces detected are :",len(self.final_faces))
        return self.final_faces
    
class Model():
    def __init__(self):
        self.model = torch.load(os.path.join(settings.BASE_DIR,'static','resources','test_model.pt'),weights_only=False,map_location=torch.device('cpu'))
    
    def preprocess(self,frames):
        preprocessed_frames = []
        transformations = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5),(0.5))
            ]
        )
        print("Came for preprocesing: ",len(frames))
        for frame in frames:
            preprocessed_frames.append(transformations(frame))
        return preprocessed_frames
    
    def predict(self,frames):
        prediction = {
            'Bored':[0],
            'Confused':[0],
            'Focused':[0],
            'Sleepy':[0],
            'Engaged':[0],
            'Not Engaged':[0],
            'total': [0]
        }
        print("Came for Prediction",len(frames))
        self.model.eval()
        # frame.to('cpu')
        for frame in frames:
            outputs = self.model(frame.unsqueeze(0))
            _, predicted = torch.max(outputs,1)
            if(predicted==0):
                prediction['Bored'][0] += 1
                prediction['Not Engaged'][0] += 1
                prediction['total'][0] +=1
                continue
            if(predicted==1):
                prediction['Confused'][0] += 1
                prediction['Engaged'][0] += 1
                prediction['total'][0] +=1

                continue
            if(predicted==2):
                prediction['Focused'][0] += 1
                prediction['Engaged'][0] += 1
                prediction['total'][0] +=1

                continue
            if(predicted==3):
                prediction['Sleepy'][0] += 1
                prediction['Not Engaged'][0] += 1
                prediction['total'][0] +=1

                
        return prediction
    