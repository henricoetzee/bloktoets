from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser, User



def login_view(request):
    if request.method != 'POST':
        return render(request, "authentication/login.html")
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "authentication/login.html", {"message": "Invalid username and/or password."})
    except Exception as e:
        return render(request, "login.html", {"message": e})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def change_password(request):
    if request.method == 'POST':
        try:
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            password_confirm = request.POST['password_confirm']
            if new_password == old_password:
                return render(request, "authentication/change_password.html", {"message": "New password should be different than old password"})
            if new_password != password_confirm:
                return render(request, "authentication/change_password.html", {"message": "New password doesn't match confirmation"})
            u = User.objects.get(username=request.user.username)
            if u.check_password(old_password):
                try:
                    u.set_password(new_password)
                    u.pw_changed = True
                    u.save()
                except Exception as e:
                    return render(request, "authentication/change_password.html", {"message": e})
                logout(request)
                return render(request, "authentication/login.html", {"message": "Password changed. Please log in again."})
            else:
                return render(request, "authentication/change_password.html", {"message": "Old password is wrong"}) 
        except Exception as e:
            return render(request, "authentication/change_password.html", {"message":e})       
    return render(request,"authentication/change_password.html" )