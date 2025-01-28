from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.


# Redirect Root Path
def reDirect(request):
    return HttpResponseRedirect('faculty')


# Intial Function
def sayHello(request):
    return render(request,'hello.html')