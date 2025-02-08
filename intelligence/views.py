from django.shortcuts import render
import time
from . import driver as dr
import cv2 as cv
from django.http import HttpResponse, StreamingHttpResponse
import pandas as pd
import os
from Class_Analytics_Generator import settings
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import io
from django.views.decorators import gzip
class Flag:
    flag = False
correct = {
    'message':"",
    'description':"",
    'title':"",
    'color':"green",
    "iconCode":"#10003"
}
wrong = {
    'message':"",
    'description':"",
    'title':"",
    'color':"#f92f60",
    "iconCode":"#10060"
}

def getGraph(request,filename):
   for i in range(12):
     while(not Flag.flag):
       pass
     dfe = pd.read_csv(os.path.join(settings.BASE_DIR,'static','resources',filename))
     row = dfe.iloc[i]
     timestamps = row['timeStamp']
     X = ["Engaged","Not Engaged","Total"]
     Y = [row['Engaged'],row['Not Engaged'],row['total']]
     plt.bar(X,Y,color=['green','red','blue'])
     plt.title("Stats for Timestamp "+timestamps)
     buf = io.BytesIO()
     plt.savefig(buf, format="jpg")
     frame = buf.getvalue()
     yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
     print(f"Generated bar for timestamps: {timestamps}")

@gzip.gzip_page
def showAnalytics(request):
     filename = request.GET.get('filename')
     graph = getGraph(request,filename)
     return StreamingHttpResponse(graph,content_type="multipart/x-mixed-replace;boundary=frame")



def startTracking(request):
     classId = request.GET.get('classId')
     facultyId = request.GET.get('facultyId')
     dateAndTime = request.GET.get('dateAndTime')
     filename = classId+"-"+facultyId+"-"+dateAndTime+'.csv'
     return render(request,'liveAnalytics.html',{'filename':filename})


def generateAnalytics(request):
     filename = request.GET.get('filename')
     classId,facultyId,dateAndTime = filename.split("-")[0],filename.split("-")[1],filename.split("-")[2]
     cam = dr.Camera()
     model = dr.Model()
     takePictureForEvery = 5
     totalDuration = 1*60
     totalFrames = totalDuration//takePictureForEvery
     for i in range(totalFrames):
          frame = cam.getFrame()
          faces = cam.detectFaces(frame)
          resized_frame = cam.resizeFrame(faces,(48,48))
          preprocessed_frames = model.preprocess(resized_frame)
          predictions = model.predict(preprocessed_frames)
          predictions['class_Id'] = [classId]
          predictions['facultyId'] = [facultyId]
          curr = str(datetime.today()).split()
          predictions['timeStamp'] = [curr[1][:8]]
          dfe = pd.DataFrame(predictions)
          if i==0:
               dfe.to_csv(os.path.join(settings.BASE_DIR,'static','resources',filename),index=False)
          else:
               dfe.to_csv(os.path.join(settings.BASE_DIR,'static','resources',filename),index=False,mode='a',header=False)

          Flag.flag = True
          print(f"Analytics {i+1} Recorded")
          Flag.flag = False
          time.sleep(takePictureForEvery)
     return HttpResponse("Sucess")
          
          



