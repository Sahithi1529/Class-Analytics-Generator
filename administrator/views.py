from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
import database_operations as db
import pandas as pd
import os
from Class_Analytics_Generator import settings
from django.core.files.storage import FileSystemStorage
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
            return HttpResponseRedirect('admin-dashboard')
        else:
            return render(request,'messenger.html',{'title':"Failure","message":"Invalid Credentials"})


def addFaculty(request):
    if request.method == "POST":
        faculty_id = request.POST.get("facultyID")
        password = request.POST.get("password")
        faculty_name = request.POST.get("facultyName")
        faculty_designation = request.POST.get("facultyDesignation")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        assigned_classes_ids = request.POST.getlist("assigned_classes")  # Multiple selections

        # Create faculty object
        faculty = FacultyData.objects.create(
            facultyID=faculty_id,
            password=password,
            facultyName=faculty_name,
            facultyDesignation=faculty_designation,
            email=email,
            phone=phone
        )

        # Assign selected classrooms
        faculty.assigned_classes.set(Classroom.objects.filter(id__in=assigned_classes_ids))
        faculty.save()

        return redirect("crudFaculty.html")  # Redirect to home page after submission

    # Fetch all classrooms to show in the dropdown
    classrooms = Classroom.objects.all()
    return render(request, "addFaculty.html", {"classrooms": classrooms})

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


# POST @/administrator/add-data-via-csv  ---> ADD DATA FROM CSV
def addDataViaCSV(request):
    if request.method !='POST':
        return HttpResponse("Not Allowed!")
    if request.session['isAuthenticated'] and request.session['role']=='admin':
        try:
           db.insert_into_table_from_file('coredb.sqlite','ADMIN',request.FILES['csvfile'])
        except:
            return HttpResponse("Sorry, unexpected error occured")
        return HttpResponse("Added Faculty Successfully!")
        

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