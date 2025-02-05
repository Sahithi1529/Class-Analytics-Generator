from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
import database_operations as db
import pandas as pd
import os
from Class_Analytics_Generator import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
# Create your views here.
def Login(request):
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    if(request.method == "GET"):
        return render(request,"adminLogin.html")
    elif(request.method == "POST"):
        entered_id = request.POST.get("adminid")
        entered_password = request.POST.get("password")
        actual_password,cols = db.retrieve_data('coredb.sqlite','ADMIN',['adminPassword'],'adminID = '+ entered_id)
        print(actual_password)
        if entered_password == actual_password[0][0]:
            request.session['isAuthenticated'] = True
            request.session['role']="admin"
            request.session['adminId'] = entered_id
            return HttpResponseRedirect('admin-dashboard')
        else:
            return render(request,'messenger.html',{'title':"Failure","message":"Invalid Credentials"})

# Test Path
def Test(request):
    return render(request,'test.html')

# Insert Data
def insertData(request):
    return render(request,'test.html')
    

# View data 
def viewData(request):
    return render(request,'test.html')

# POST @/administrator/update-model  ---> UPDATE THE PREDICTING MODEL
def updateModel(request):
    if request.method!='POST':
        return HttpResponse("Not Allowed")
    new_model = request.FILES['model']
    # os.rename(new_model,str(settings.BASE_DIR)+'/predictormodel.csv')
    FileSystemStorage(location=settings.BASE_DIR).save(new_model.name, new_model)
    return HttpResponse("Model Updated Successfully")
    
# GET @/administrator/admin-dashboard   ---> ADMIN DASHBOARD
def adminDashboard(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin':
        request.session['isAuthenticated'] - False
        request.session['role'] = None
        return HttpResponse("Access Blockeed")
    return render(request,'adminHome.html')

# GET @/administrator/logout  ---> LOGOUT
def logout(request):
    if request.method != 'GET':
        return HttpResponse("Accessing URL is allowed only with GET request")
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    return HttpResponseRedirect('/administrator/')


# POST @/administrator/add-faculty-via-csv  ---> ADD FACULTY DATA FROM CSV
def addFacultyViaCSV(request):
    if request.method !='POST':
        return HttpResponse("Not Allowed!")
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        try:
           db.insert_into_table_from_file('coredb.sqlite','FACULTY',request.FILES['csvfile'])
        except:
            return HttpResponse("Sorry, unexpected error occured")
        return HttpResponse("Added Faculty Successfully!")
    

# POST @/administrator/add-admin-via-csv  ---> ADD ADMIN DATA FROM CSV
def addAdminViaCSV(request):
    if request.method !='POST':
        return HttpResponse("Not Allowed!")
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        try:
           db.insert_into_table_from_file('coredb.sqlite','ADMIN',request.FILES['csvfile'])
        except:
            return HttpResponse("Sorry, unexpected error occured")
        return HttpResponse("Added Admins Successfully!")
        
        

# GET @/adiministrator/download-data  ---> DOWNLOAD FACULTY DATA
def downloadData(request):
    if request.method !='GET':
        return render(request,'messenger.html',{"title":"Prohibited","message":"Prohibited"})
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        # User Allowed to Download the data
        db.download_data_as_csv('coredb.sqlite','ADMIN','static/faculty.csv')
        return render(request,'forDownload.html')
    else:
        # User not Allowed o Download the data
        return render(request,'messenger.html',{'title':"Download prohibited",'message':"You cannot download the file"})
    
# GET @/administrator/view-messages  ---> SEE MESSAGES IN INBOX
def viewMessages(request):
     if not request.session['isAuthenticated'] or request.session['role']!='admin':
        return HttpResponse("Access Blocked")
     if request.method !='GET':
         return HttpResponse("Only GET Requests are accepted")
     try:
         rows,cols = db.retrieve_data('coredb.sqlite','MESSAGES',['SenderId','SentDate','SentTime','Message'],'ReceiverId = '+ str(request.session['adminId']))
         context = []
         for row in rows:
             k = {}
             k['sender'] = row[0]
             k['date'] = row[1]
             k['time'] = row[2]
             k['message'] = row[3]
             context.append(k)
         return render(request,'viewMessages.html',{'messages':context})
     except Exception as e:
         print(f"Exception '{e}' Occured")
         return HttpResponse("Sorry Try again!!")
     
# POST @/administrator/send-message  ---> SEND MESSAGE TO THE ADMIN
def sendMessage(request):
     if not request.session['isAuthenticated'] or request.session['role']!='admin':
        return HttpResponse("Access Blocked")
     if request.method !='POST':
         return HttpResponse("Only Post Requests are accepted")
     message = request.POST.get('message')
     sender = request.session['adminId']
     receiver = request.POST.get('receiverId')
     curr = str(datetime.today()).split()
     date = curr[0]
     time = curr[1][:8]
     print(sender,receiver,date,time,message)
     rows = [[int(sender),int(receiver),date,time,message]]
     try:
         if db.insert_into_table('coredb.sqlite','MESSAGES',rows):
            return HttpResponse("Message Sent Successfully")
         else:
            return HttpResponse("Message is not sent")
     
     except Exception as e:
         print(f"Exception '{e}' Occurred when inserting data into Messages")
         return HttpResponse("Message is not sent")
     
# GET @/administrator/view-faculty   ---> DISPLAY FACULTY LIST
def viewFaculty(request):
     if not request.session['isAuthenticated'] or request.session['role']!='admin':
        return HttpResponse("Access Blocked")
     if request.method !='GET':
         return HttpResponse("Only Get Requests are accepted")
     faculty,cols = db.retrieve_data('coredb.sqlite','FACULTY',['FacultyId','FacultyName','FacultyDepartment'])
     context = []
     for (fid,fname,fdept) in faculty:
         k = {}
         k['facultyId'] = fid
         k['facultyName'] = fname
         k['facultyDepartment'] = fdept
         k['generate'] = '/administrator/generate-analytics?'+str(fid)
         context.append(k)
     return render(request,'viewFaculty.html',{'context':context})