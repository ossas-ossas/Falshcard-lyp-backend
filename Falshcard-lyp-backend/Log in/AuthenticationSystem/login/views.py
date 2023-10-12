from django.shortcuts import render

from login.models import RegisterUser
from django.shortcuts import redirect


# Create your views here.

def index(request):
    login_msg = "login successfully"
    return render(request, "index.html", {"login_msg":login_msg})

def register(request):
    if request.method == "POST":
        # get the user mame and password
        userName = request.POST.get("username")
        userPassword = request.POST.get("userpassword")
        userRePassword = request.POST.get("userrepassword")
        try:
            # get user info from database
            user=RegisterUser.objects.get(reg_name=userName)
            # user already exist then return to home page
            if user:
                msg = "user already exist"
                return render(request, "register.html", {"msg":msg})
        except:
            # password does not match to rePassword
            # then return to register page and try again
            if userPassword != userRePassword:
                error_msg = "passwords not the same"
                return render(request, "register.html", {"error_msg":error_msg})
        else:
            # successfully entered username and pwd, save the user info into database
            register = RegisterUser()
            # save the username and user psw to the database
            register.reg_name = userName
            register.reg_pwd = userPassword
            register.save()
            return redirect("/login/")
    else:
        return render(request, "register.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if register.method == "POST":
        # get the input from the web page
        userName = request.POST.get("username")
        userPassword = request.POST.get("userpassword")
        try:
            # retrieve user info from database
            user = RegisterUser.objects.get(reg_name=userName)
            # correct pwd => login
            if userPassword == user.reg_pwd:
                return redirect("/index/")
            # wrong pwd => try login again
            else:
                error_msg = "wrong password"
                return render(request, "login_html", {"error_msg":error_msg})
        # username does not exist => return to login page and try again
        except:
            error_msg = "user not exist"
            return render(request, "login.html", {"error_msg":error_msg})

