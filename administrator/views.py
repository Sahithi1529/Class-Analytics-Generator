from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
import database_operations as db
import pandas as pd
import os
from Class_Analytics_Generator import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
correct = {
    'color':"green",
    "iconCode":"#10003"
}
wrong = {
    'color':"#f92f60",
    "iconCode":"#10060"
}

# GET/POST @/administrator/     ---> ADMIN LOGIN
def Login(request):
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    if(request.method == "GET"):
        return render(request,"Login.html",{ 'role':'Admin'})
    elif(request.method == "POST"):
        entered_id = request.POST.get("Adminid")
        entered_password = request.POST.get("password")
        actual_password,cols = db.retrieve_data('coredb.sqlite','ADMIN',['adminPassword','adminName'],'adminID = '+ entered_id)
        if entered_password == actual_password[0][0]:
            request.session['isAuthenticated'] = True
            request.session['role']="admin"
            request.session['adminId'] = entered_id
            request.session['adminName'] = actual_password[0][1]
            return HttpResponseRedirect('admin-dashboard')
        else:
            wrong['title'] ='Failure'
            wrong['message'] = "Invalid Credentials"
            return render(request,'messenger.html',wrong)

# GET @/administrator/admin-dashboard   ---> ADMIN DASHBOARD
def adminDashboard(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin' or request.method!='GET':
        request.session['isAuthenticated'] = False
        request.session['role'] = None
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blockeed"
        return render(request,'messenger.html',wrong)
    return render(request,'adminDashboard.html',{'name':request.session['adminName']})

# GET @/adiministrator/download-data  ---> DOWNLOAD DATA FROM DATABASE AS CSV
def downloadData(request):
    if request.method !='GET':
        wrong['title'] ='Prohibited'
        wrong['message'] = "Prohibited"
        return render(request,'messenger.html',wrong)
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        # User Allowed to Download the data
        table = request.GET.get('download-what')
        db.download_data_as_csv('coredb.sqlite',table,os.path.join(settings.BASE_DIR,'static','resources',f'{table}.csv'))
        return render(request,'forDownload.html',{'file':table})
    else:
        # User not Allowed o Download the data
        wrong['title'] ='Download prohibited'
        wrong['message'] = "You cannot download the file"
        return render(request,'messenger.html',wrong)

# GET @/administrator/logout  ---> LOGOUT
def logout(request):
    if request.method != 'GET':
        wrong['title'] ='Failure'
        wrong['message'] = "Accessing URL is allowed only with GET request"
        return render(request,'messenger.html',wrong)
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    return HttpResponseRedirect('/administrator/')
    
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
         rows,cols = db.retrieve_data('coredb.sqlite','MESSAGES',['SenderId','SentDate','SentTime','Message'],f"RECEIVERID = {request.session['adminId']} OR SENDERID={request.session['adminId']}")
         context = []
         for i in range(1,len(rows)+1):
             row = rows[-i]
             k = {}
             k['sender'] = row[0]
             k['date'] = row[1]
             k['time'] = row[2]
             k['message'] = row[3]
             k['adminId'] = int(request.session['adminId'])
             context.append(k)
         return render(request,'viewMessagesAdmin.html',{'messages':context,'name':request.session['adminName']})
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
     receiver = request.POST.get('facultyId')
     curr = str(datetime.today()).split()
     date = curr[0]
     time = curr[1][:8]
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
         k['generate'] = '/administrator/generate-analytics?facultyId='+str(fid)
         context.append(k)
     return render(request,'viewFaculty.html',{'context':context,'name':request.session['adminName']})

# POST @/administrator/   --> UPDATE MODEL
def updateModel(request):
    new_model = request.FILES['model']
    FileSystemStorage(location=os.path.join(settings.BASE_DIR,'static','resources')).save(new_model.name, new_model)
    correct['title'] ='Success'
    correct['message'] = "Model Updated Successfully"
    return render(request,'messenger.html',correct)

# GET @/administrator/update-manually ---> SHOW FORM TO UPDATE MANUALLY
def updateManually(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    
    if request.method !='GET':
         wrong['title'] ='Failure'
         wrong['message'] = "Only GET requests are accepted"
         return render(request,'messenger.html',wrong)
    
    parameter = request.GET.get('update-what')

    if parameter == "model":
        return updateModel(request)

    reference = {
        'admin':['AdminId','AdminName','AdminEmail','AdminPassword','AdminDepartment','AdminPhone'],
        'faculty':['FacultyId','FacultyName','FacultyEmail','FacultyPassword','FacultyDepartment','FacultyPhone'],
        'classroom':['Department','Year','Section','Classid'],
        'course':['Subjectid','Subjectname'],
        'mapping':['Facultyid','Subjectid','Classid']
    }
    return render(request,'updateManually.html',{'fields':reference[parameter],'updateWhat':parameter,'name':request.session['adminName']})

# POST @/administrator/updatethem   --> UPDATE MANUALLY
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

def updatePassword(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    if request.method !='POST':
        return render(request,'updatePasswordAdmin.html',{'name':request.session['adminName'],'role':'admin'})
    entered_curr_password = request.POST.get('currentPassword')
    entered_new_password = request.POST.get('newPassword')
    actual_password,cols = db.retrieve_data('coredb.sqlite','ADMIN',['adminPassword'],'adminID = '+ request.session['adminId'])
    if str(entered_curr_password) == str(actual_password[0][0]):
        status = db.update_data('coredb.sqlite','ADMIN',{'adminPassword':entered_new_password},' ADMINID = '+str(request.session['adminId']))
        if status:
            correct['title'] = "Success"
            correct['message'] = "Password update successfully"
            return render(request,'messenger.html',correct)
        else:
            wrong['title'] = "Failure"
            wrong['message'] = "Sorry could not update password. Try Again"
            return render(request,'messenger.html',wrong)

    else:
        wrong['title'] = "Failure"
        wrong['message'] = "Please enter correct current password!!"
        return render(request,'messenger.html',wrong)
    

# GET @/administrator/manage-database   ---> MANAGE DATABASE
def manageDatabase(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin' or request.method!='GET':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    return render(request,'updateDB.html',{'name':request.session['adminName']})

def addViaCSV(request):
    if request.method !='POST':
        wrong['title'] ='Failure'
        wrong['message'] = "Not Allowed!"
        return render(request,'messenger.html',wrong)
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        table = request.POST.get('update-what')
        try:
           db.insert_into_table_from_file('coredb.sqlite',table,request.FILES['csvfile'])
        except Exception as e:
            print(e)
            wrong['title'] ='Failure'
            wrong['message'] = "Sorry, unexpected error occured"
            return render(request,'messenger.html',wrong)
        correct['title'] ='Success'
        correct['message'] = f"Added {table} Successfully"
        return render(request,'messenger.html',correct)
    
# GET @/administrator/generate-analytics?facultyId   ---> Show Excel File to download and show pie chart
# Pie Chart for Average
# Excel file for each completed class
def generateAnalytics(request):
    if not request.session['isAuthenticated'] or request.session['role']!='admin' or request.method!="GET":
        wrong['title'] = "Failure"
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    # User is allowed to view stats
    facultyId = request.GET.get('facultyId')
    mappings, cols = db.retrieve_data('coredb.sqlite','MAPPING',["*"],f'FACULTYID = {facultyId} AND COMPLETED = 1') # 1 means completed
    file_names = []
    classIds = []
    dates = []
    for mapping in mappings:
       filename = str(mapping[2])+"-"+str(facultyId)+"-"+str(mapping[4])+'.csv'
       file_names.append(filename)
       classIds.append(mapping[2])
       dates.append(mapping[4])
    context = []
    for i in range(len(file_names)):
        k = {}
        k['classId'] = classIds[i]
        k['date'] = dates[i]
        k['filename'] = file_names[i]
        context.append(k)
    return render(request,'displayAnalytics.html',{'context':context,'name':request.session['adminName'],'facultyId':facultyId})
    


    