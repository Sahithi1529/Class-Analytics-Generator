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

# GET @/intelligence/start-tracking  ---> Starts recording stats
def startTracking(request):
     classId = request.GET.get('classId')
     facultyId = request.GET.get('facultyId')
     dateAndTime = request.GET.get('dateAndTime')
     filename = classId+"-"+facultyId+"-"+dateAndTime+".csv"
     takePictureForEvery = 5
     totalDuration = 1*60
     totalFrames = totalDuration//takePictureForEvery
     cam = dr.Camera()
     model = dr.Model()
     for i in range(totalFrames):
          frame = cam.getFrame()
          resized_frame = cam.resizeFrame(frame,(48,48))
        #   preprocessed_frame = model.preprocess(resized_frame)
          preprocessed_frame = resized_frame
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
     correct['title'] = "Class Completed"
     correct['message'] = "Class Analytics Generated Successfully!!"
     return render(request,'messenger.html',correct)

# GET @/intelligence/generate-analytics   ---> Generate Analytics from CSV File
def generateAnalytics(request):
     filename = request.GET.get('filename')
     dfe = pd.read_csv(os.path.join(settings.BASE_DIR,'static','resources',filename))
     timestamps = dfe.iloc[:]['timeStamp']
     values = {
          'Engaged':dfe.iloc[:]['Engaged'],
          'Not Engaged':dfe.iloc[:]['Not Engaged'],
          'Total':dfe.iloc[:]['total']
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
     ax.set_ylabel('Count of Students')
     ax.set_title('Time Stamps')
     ax.set_xticks(x + width, timestamps)
     ax.legend(loc='upper left', ncols=3)
     ax.set_ylim(0, 80)
     plt.savefig(os.path.join(settings.BASE_DIR,'static','resources','analytics.png'))
     return render(request,'showAnalytics.html',{'filename':filename})


def getGraph(filename):
     
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
     yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def showAnalytics(request):
     filename = request.GET.get('filename')
     graph = getGraph(filename)
     return StreamingHttpResponse(graph,content_type="multipart/x-mixed-replace;boundary=frame")

















def Test(request):
    class_Id = request.GET.get('classId')
    faculty_Id = request.GET.get('facultyId')
    dateAndTime = request.GET.get('dateTime')
    # cam = dr.Camera()
    # model = dr.Model()
    # frame = cam.getFrame() # We will have a gray scale image
    # resized_frame = cam.resizeFrame(frame,(48,48))
    # preprocessed_frame = model.preprocess(resized_frame)
    # prediction = model.predict(preprocessed_frame) # Let us put it as Dictionary
    for i in range(5):
        prediction = {
            'Bored':[2],
            'Confused':[3],
            'Focused':[4],
            'Sleepy':[1],
            'Engaged':[7],
            'Not Engaged':[3],
            'total': [10]
        }
        prediction['class_Id'] = [class_Id]
        prediction['facultyId'] = [faculty_Id]
        curr = str(datetime.today()).split()
        prediction['timeStamp'] = [curr[1][:8]]
        filename = class_Id+"-"+faculty_Id+"-"+dateAndTime+'.csv'
        if filename in os.listdir(os.path.join(settings.BASE_DIR,'static','resources')):
             dfe = pd.DataFrame(prediction)
             dfe.to_csv(os.path.join(settings.BASE_DIR,'static','resources',filename),mode='a', index=False, header=False)
        else:
            dfe = pd.DataFrame(prediction)
            dfe.to_csv(os.path.join(settings.BASE_DIR,'static','resources',filename),index=False)
        print("DONE")
        time.sleep(5)
    return HttpResponse("Hello")




