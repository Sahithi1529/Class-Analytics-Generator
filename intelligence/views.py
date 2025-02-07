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
     dfe = pd.read_csv(os.path.join(settings.BASE_DIR,'static','resources',filename))
     timestamps = dfe.iloc[:]['timeStamp']
     values = {
     'Engaged' : dfe.iloc[:]['Engaged'],
     'Not Engaged' : dfe.iloc[:]['Not Engaged'],
     'Total' : dfe.iloc[:]['total'],
     }
     x = np.arange(len(timestamps))  # the label locations
     width = 0.25  # the width of the bars
     multiplier = 0
     fig, ax = plt.subplots(layout='constrained')
     ref = {
     'Engaged':"green",
     "Not Engaged":"red",
     "Total":"blue"
     }

     for attribute, measurement in values.items():
          offset = width * multiplier
          rects = ax.bar(x + offset, measurement, width, label=attribute,color=ref[attribute])
          ax.bar_label(rects, padding=3)
          multiplier += 1
     # Add some text for labels, title and custom x-axis tick labels, etc.
     ax.set_ylabel('Count of Students')
     ax.set_title('Time Stamps')
     ax.set_xticks(x + width, timestamps)
     ax.legend(loc='upper left', ncols=3)
     ax.set_ylim(0, 80)
     buf = io.BytesIO()
     plt.savefig(buf, format="jpg")
     frame = buf.getvalue()
     time.sleep(5)
     if i==11:
         correct['title'] = "Success"
         correct['Message'] = "Class Analytics generated successfully"
         return render(request,'messenger.html',correct)
     yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def showAnalytics(request):
     filename = request.GET.get('filename')
     time.sleep(10)
     graph = getGraph(request,filename)
     print("Hello")
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
          resized_frame = cam.resizeFrame(frame,(48,48))
          preprocessed_frame = model.preprocess(resized_frame)
          predictions = model.predict(preprocessed_frame)
          predictions['class_Id'] = [classId]
          predictions['facultyId'] = [facultyId]
          curr = str(datetime.today()).split()
          predictions['timeStamp'] = [curr[1][:8]]
          dfe = pd.DataFrame(predictions)
          if i==0:
               dfe.to_csv(os.path.join(settings.BASE_DIR,'static','resources',filename),index=False)
          else:
               dfe.to_csv(os.path.join(settings.BASE_DIR,'static','resources',filename),index=False,mode='a',header=False)

          print(f"Analytics {i} Recorded")
          time.sleep(takePictureForEvery)
     return HttpResponse("Sucess")
          
          



