from django.shortcuts import render, redirect
from .models import FacultyData, Classroom


# Create your views here.
def Login(request):
    if(request.method == "GET"):
        return render(request,"adminLogin.html")
    elif(request.method == "POST"):
        entered_id = request.POST.get("adminid")
        entered_password = request.POST.get("password")
        if entered_id == "101" and entered_password == "123":
            return render(request, "crudFaculty.html")
        

    #         return render(request,"messenger.html",{'title':"Success",'message':"Login Success"})
    #     else:
    #         return render(request,"messenger.html",{'title':"Failed",'message':"Wrong Credentials"})
    # else:
    #     return render(request,"messenger.html",{'title':"Not Allowed 🚫",'message':"Unauthozied Access 🚫"})


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





