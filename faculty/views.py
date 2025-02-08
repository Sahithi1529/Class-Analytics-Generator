from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import database_operations as db
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


# Redirect Root Path
def reDirect(request):
    return HttpResponseRedirect('faculty')



# GET/POST @/faculty/  --> FACULTY LOGIN
def facultyLogin(request):
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    if(request.method == "GET"):
        return render(request,"Login.html",{ 'role':'Faculty'})
    elif(request.method == "POST"):
        entered_id = request.POST.get("Facultyid")
        entered_password = request.POST.get("password")
        actual_password,cols = db.retrieve_data('coredb.sqlite','FACULTY',['facultyPassword','facultyName'],'facultyID = '+ entered_id)
        if entered_password == actual_password[0][0]:
            request.session['isAuthenticated'] = True
            request.session['role']="faculty"
            request.session['facultyId'] = entered_id
            request.session['facultyName'] = actual_password[0][1]
            return HttpResponseRedirect('faculty-dashboard')
        else:
            wrong['title'] ='Failure'
            wrong['message'] = "Invalid Credentials"
            return render(request,'messenger.html',wrong)
        
# GET @/faculty/faculty-dashboard  ---> FACULTY DASHBOARD
def facultyDashboard(request):
    if not request.session['isAuthenticated'] or request.session['role']!='faculty':
            wrong['title'] ='Failure'
            wrong['message'] = "Access Blocked"
            return render(request,'messenger.html',wrong)
    return render(request,'facultyDashboard.html',{'name':request.session['facultyName']})

# GET @/faculty/logout  ---> LOGOUT
def logout(request):
    if request.method != 'GET':
            wrong['title'] ='Failure'
            wrong['message'] = "Accessing URL is allowed only with GET request"
            return render(request,'messenger.html',wrong)
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    return HttpResponseRedirect('/faculty/')

# POST @/faculty/send-message  ---> SEND MESSAGE TO THE ADMIN
def sendMessage(request):
     if not request.session['isAuthenticated'] or request.session['role']!='faculty':
            wrong['title'] ='Failure'
            wrong['message'] = "Access Blockec"
            return render(request,'messenger.html',wrong)
     if request.method !='POST':
        wrong['title'] ='Failure'
        wrong['message'] = "Only POST requests are accepted"
        return render(request,'messenger.html',wrong)
     message = request.POST.get('message')
     sender = request.session['facultyId']
     receivers,cols = db.retrieve_data('coredb.sqlite','ADMIN',['adminId'])
     curr = str(datetime.today()).split()
     date = curr[0]
     time = curr[1][:8]
     rows = []
     for receiver in receivers:
         rows.append([int(sender),receiver[0],date,time,message])
     print(rows)
     try:
         if db.insert_into_table('coredb.sqlite','MESSAGES',rows):
            correct['title'] = "Success"
            correct['message'] = "Message Sent Successfully!!"
            return render(request,'messenger.html',correct)
         else:
            wrong['title'] ='Failure'
            wrong['message'] = "Message is not sent"
            return render(request,'messenger.html',wrong)
     
     except Exception as e:
        print(f"Exception '{e}' Occurred when inserting data into Messages")
        wrong['title'] ='Failure'
        wrong['message'] = "Message is not sent"
        return render(request,'messenger.html',wrong)
     
# GET @/faculty/view-messages  ---> SEE MESSAGES IN INBOX
def viewMessages(request):
     if not request.session['isAuthenticated'] or request.session['role']!='faculty':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
     if request.method !='GET':
        wrong['title'] ='Failure'
        wrong['message'] = "Only GET requests are accepted!!"
        return render(request,'messenger.html',wrong)
     try:
         rows,cols = db.retrieve_data('coredb.sqlite','MESSAGES',['SenderId','SentDate','SentTime','Message'],'ReceiverId = '+ str(request.session['facultyId']+" OR SenderId="+str(request.session['facultyId'])))
         context = []
         for row in rows:
             k = {}
             k['sender'] = row[0]
             k['date'] = row[1]
             k['time'] = row[2]
             k['message'] = row[3]
             k['facultyId'] = int(request.session['facultyId'])
             context.append(k)
         return render(request,'viewMessages.html',{'messages':context,'name':request.session['facultyName']})
     except Exception as e:
        print(f"Exception '{e}' Occured")
        wrong['title'] ='Failure'
        wrong['message'] = "Sorry Try again!!"
        return render(request,'messenger.html',wrong)
     

# GET @/faculty/view-courses   ---> VIEW COURSES OF FACULTY
def viewCourses(request):
     if not request.session['isAuthenticated'] or request.session['role']!='faculty':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
     if request.method !='GET':
        wrong['title'] ='Failure'
        wrong['message'] = "Only GET requests are accepted!!"
        return render(request,'messenger.html',wrong)
     date = str(datetime.today()).split()[0]
     courses,cols = db.retrieve_data('coredb.sqlite','MAPPING',['*'],f"FACULTYID = {str(request.session['facultyId'])}  AND CLASSDATE = '{str(date)}'")
     classes = []
     subjects = []
     classId = []
     for course in courses:
         classi = course[2]
         subject = course[1]
         subject,cols = db.retrieve_data('coredb.sqlite','COURSE',['subjectname'],'SUBJECTID ='+str(subject))
         classi,cols = db.retrieve_data('coredb.sqlite','CLASSROOM',['year','department','section'],'CLASSID ='+str(classi))
         class_name = " ".join(classi[0])
         classes.append(class_name)
         subjects.append(subject[0][0])
         classId.append(str(course[2]))
     context  = []
     for i in range(len(classes)):
         k = {}
         k['classname'] = classes[i]
         k['subject'] = subjects[i]
         k['classId'] = classId[i]
         k['facultyId'] = request.session['facultyId']
         k['dateAndTime'] = date
         context.append(k)
     return render(request,'viewCourses.html',{'courses':context,'name':request.session['facultyName']})


# POST @/faculty/update-password   -->  UPDATE THE FACULTY PASSWORD
def updatePassword(request):
    if not request.session['isAuthenticated'] or request.session['role']!='faculty':
        wrong['title'] ='Failure'
        wrong['message'] = "Access Blocked"
        return render(request,'messenger.html',wrong)
    if request.method !='POST':
        wrong['title'] ='Failure'
        wrong['message'] = "Only POST requests are accepted!!"
        return render(request,'messenger.html',wrong)
    entered_curr_password = request.POST.get('currentPassword')
    entered_new_password = request.POST.get('newPassword')
    actual_password,cols = db.retrieve_data('coredb.sqlite','FACULTY',['facultyPassword','facultyName'],'facultyID = '+ request.session['facultyId'])
    if entered_curr_password == actual_password:
        status = db.update_data('coredb.sqlite','FACULTY',{'facultyPassword':entered_new_password},' FACULTYID = '+str(request.session['facultyId']))
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
    




     
         

    
