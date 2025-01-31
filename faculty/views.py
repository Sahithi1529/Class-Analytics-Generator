from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.


# Redirect Root Path
def reDirect(request):
    return HttpResponseRedirect('faculty')


# Intial Function
def facultyLogin(request):
    return render(request,'facultyLogin.html')

def homePage(request):
    entered_id = request.POST.get("facultyid")
    entered_password = request.POST.get("password")
    
