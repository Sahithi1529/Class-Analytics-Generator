from django.shortcuts import render

# Create your views here.
def Login(request):
    if(request.method == "GET"):
        return render(request,"adminLogin.html")
    elif(request.method == "POST"):
        entered_id = request.POST.get("adminid")
        entered_password = request.POST.get("password")
        if entered_id == "101" and entered_password == "123":
            return render(request,"messenger.html",{'title':"Success",'message':"Login Success"})
        else:
            return render(request,"messenger.html",{'title':"Failed",'message':"Wrong Credentials"})
    else:
        return render(request,"messenger.html",{'title':"Not Allowed 🚫",'message':"Unauthozied Access 🚫"})