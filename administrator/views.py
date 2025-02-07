from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
import database_operations as db
import pandas as pd
import os
from Class_Analytics_Generator import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
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
            wrong['title'] ='Failure'
            wrong['message'] = "Invalid Credentials"
            return render(request,'messenger.html',wrong)

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
        wrong['title'] ='Failure'
        wrong['message'] = "Only POST Requests are allowed"
        return render(request,'messenger.html',wrong)
    new_model = request.FILES['model']
    FileSystemStorage(location=os.path.join(settings.BASE_DIR,'static','resources')).save(new_model.name, new_model)
    correct['title'] ='Success'
    correct['message'] = "Model Updated Successfully"
    return render(request,'messenger.html',correct)
    
# GET @/administrator/admin-dashboard   ---> ADMIN DASHBOARD
def adminDashboard(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin':
        request.session['isAuthenticated'] - False
        request.session['role'] = None
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blockeed"
        return render(request,'messenger.html',wrong)
    return render(request,'adminHome.html')

# GET @/administrator/logout  ---> LOGOUT
def logout(request):
    if request.method != 'GET':
        wrong['title'] ='Failure'
        wrong['message'] = "Accessing URL is allowed only with GET request"
        return render(request,'messenger.html',wrong)
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    return HttpResponseRedirect('/administrator/')


# POST @/administrator/add-faculty-via-csv  ---> ADD FACULTY DATA FROM CSV
def addFacultyViaCSV(request):
    if request.method !='POST':
        wrong['title'] ='Failure'
        wrong['message'] = "Not Allowed!"
        return render(request,'messenger.html',wrong)
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        try:
           db.insert_into_table_from_file('coredb.sqlite','FACULTY',request.FILES['csvfile'])
        except:
            wrong['title'] ='Failure'
            wrong['message'] = "Sorry, unexpected error occured"
            return render(request,'messenger.html',wrong)
        correct['title'] ='Success'
        correct['message'] = "Added Faculty Successfully"
        return render(request,'messenger.html',correct)
    

# POST @/administrator/add-admin-via-csv  ---> ADD ADMIN DATA FROM CSV
def addAdminViaCSV(request):
    if request.method !='POST':
        wrong['title'] ='Failure'
        wrong['message'] = "Not Allowed!"
        return render(request,'messenger.html',wrong)
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        try:
           db.insert_into_table_from_file('coredb.sqlite','ADMIN',request.FILES['csvfile'])
        except:
            wrong['title'] ='Failure'
            wrong['message'] = "Sorry, unexpected error occured"
            return render(request,'messenger.html',wrong)
        correct['title'] ='Success'
        correct['message'] = "Added Admin Successfully"
        return render(request,'messenger.html',correct)
        
        

# GET @/adiministrator/download-data  ---> DOWNLOAD FACULTY DATA
def downloadData(request):
    if request.method !='GET':
        wrong['title'] ='Prohibited'
        wrong['message'] = "Prohibited"
        return render(request,'messenger.html',wrong)
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        # User Allowed to Download the data
        db.download_data_as_csv('coredb.sqlite','ADMIN',os.path.join(settings.BASE_DIR,'static','resources','faculty.csv'))
        return render(request,'forDownload.html')
    else:
        # User not Allowed o Download the data
        wrong['title'] ='Download prohibited'
        wrong['message'] = "You cannot download the file"
        return render(request,'messenger.html',wrong)
    
# GET @/administrator/view-messages  ---> SEE MESSAGES IN INBOX
def viewMessages(request):
     if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked!"
        return render(request,'messenger.html',wrong)
     if request.method !='GET':
        wrong['title'] ='Failure'
        wrong['message'] = "Only GET Requests are accepted"
        return render(request,'messenger.html',wrong)
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
         wrong['title'] ='Failure'
         wrong['message'] = "Sorry Try again!!"
         return render(request,'messenger.html',wrong)
     
# POST @/administrator/send-message  ---> SEND MESSAGE TO THE ADMIN
def sendMessage(request):
     if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked!"
        return render(request,'messenger.html',wrong)
     if request.method !='POST':
        wrong['title'] ='Failure'
        wrong['message'] = "Only POST Requests are accepted"
        return render(request,'messenger.html',wrong)
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
            correct['title'] ='Message Sent'
            correct['message'] = "Message Sent Successfully!!"
            return render(request,'messenger.html',correct)
         else:
            wrong['title'] ='Failure'
            wrong['message'] = "Message Not Sent"
            return render(request,'messenger.html',wrong)
     
     except Exception as e:
         print(f"Exception '{e}' Occurred when inserting data into Messages")
         wrong['title'] ='Failure'
         wrong['message'] = "Message Not Sent"
         return render(request,'messenger.html',wrong)
     
# GET @/administrator/view-faculty   ---> DISPLAY FACULTY LIST
def viewFaculty(request):
     if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
     if request.method !='GET':
         wrong['title'] ='Failure'
         wrong['message'] = "Only GET requests are accepted"
         return render(request,'messenger.html',wrong)
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

# GET @/administrator/update-manually ---> UPDATE DATABASE MANUALLY
def updateManually(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    
    if request.method !='GET':
         wrong['title'] ='Failure'
         wrong['message'] = "Only GET requests are accepted"
         return render(request,'messenger.html',wrong)
    
    parameter = request.GET.get('updateWhat')
    reference = {
        'admin':['AdminId','AdminName','AdminEmail','AdminPassword','AdminDepartment','AdminPhone'],
        'faculty':['FacultyId','FacultyName','FacultyEmail','FacultyPassword','FacultyDepartment','FacultyPhone'],
        'classroom':['Department','Year','Section','Classid'],
        'course':['Subjectid','Subjectname'],
        'mapping':['Facultyid','Subjectid','Classid']
    }
    return render(request,'updateManually.html',{'fields':reference[parameter],'updateWhat':parameter})

# POST @/administrator/updatethem
def updateThem(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    
    if request.method !='POST':
         wrong['title'] ='Failure'
         wrong['message'] = "Only POST requests are accepted"
         return render(request,'messenger.html',wrong)
    reference = {
        'admin':['AdminId','AdminName','AdminEmail','AdminPassword','AdminDepartment','AdminPhone'],
        'faculty':['FacultyId','FacultyName','FacultyEmail','FacultyPassword','FacultyDepartment','FacultyPhone'],
        'classroom':['Department','Year','Section','Classid'],
        'course':['Subjectid','Subjectname'],
        'mapping':['Facultyid','Subjectid','Classid']
    }
    parameter = request.POST.get('updateWhat')
    columns = reference[parameter]
    row = []
    for i in columns:
        row.append(request.POST.get(i))
    try:
        db.insert_into_table('coredb.sqlite',parameter,[row])
        correct['title'] = "Success"
        correct['message'] = parameter +" added Successfully!!"
        return render(request,'messenger.html',correct)
    except:
        wrong['title'] = "failure"
        wrong['message'] = "Unable to Add "+parameter
        return render(request,'messenger.html',wrong)

    