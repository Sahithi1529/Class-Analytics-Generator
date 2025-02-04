from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import database_operations as db
from datetime import datetime

# Create your views here.


# Redirect Root Path
def reDirect(request):
    return HttpResponseRedirect('faculty')



# GET/POST @/faculty/  --> FACULTY LOGIN
def facultyLogin(request):
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    if(request.method == "GET"):
        return render(request,"facultyLogin.html")
    elif(request.method == "POST"):
        entered_id = request.POST.get("facultyid")
        entered_password = request.POST.get("password")
        actual_password,cols = db.retrieve_data('coredb.sqlite','FACULTY',['facultyPassword'],'facultyID = '+ entered_id)
        print(actual_password)
        if entered_password == actual_password[0][0]:
            request.session['isAuthenticated'] = True
            request.session['role']="faculty"
            request.session['facultyId'] = entered_id
            return HttpResponseRedirect('faculty-dashboard')
        else:
            return render(request,'messenger.html',{'title':"Failure","message":"Invalid Credentials"})

# GET @/faculty/faculty-dashboard  ---> FACULTY DASHBOARD
def facultyDashboard(request):
    if not request.session['isAuthenticated'] or request.session['role']!='faculty':
        return HttpResponse("Access Blocked")
    return render(request,'facultyHome.html')

# GET @/faculty/logout  ---> LOGOUT
def logout(request):
    if request.method != 'GET':
        return HttpResponse("Accessing URL is allowed only with GET request")
    request.session['isAuthenticated'] = False
    request.session['role'] = None
    return HttpResponseRedirect('/faculty/')

# POST @/faculty/send-message  ---> SEND MESSAGE TO THE ADMIN
def sendMessage(request):
     if not request.session['isAuthenticated'] or request.session['role']!='faculty':
        return HttpResponse("Access Blocked")
     if request.method !='POST':
         return HttpResponse("Only Post Requests are accepted")
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
            return HttpResponse("Message Sent Successfully")
         else:
            return HttpResponse("Message is not sent")
     
     except Exception as e:
         print(f"Exception '{e}' Occurred when inserting data into Messages")
         return HttpResponse("Message is not sent")
     
# GET @/faculty/view-messages  ---> SEE MESSAGES IN INBOX
def viewMessages(request):
     if not request.session['isAuthenticated'] or request.session['role']!='faculty':
        return HttpResponse("Access Blocked")
     if request.method !='GET':
         return HttpResponse("Only Post Requests are accepted")
     try:
         rows,cols = db.retrieve_data('coredb.sqlite','MESSAGES',['SenderId','SentDate','SentTime','Message'],'ReceiverId = '+ str(request.session['facultyId']))
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


     
         

    
