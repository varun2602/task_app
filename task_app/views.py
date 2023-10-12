from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
import json
from . import models


@login_required(login_url="http://127.0.0.1:8000/login_view/")
def index(request):
    tasks_all = models.Task.objects.filter(user = request.user)
    return render(request, "index.html")

def create_task(request):
    pass 

def update_task(request):
    pass 

def delete_task(request):
    pass
@csrf_exempt
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)

        # Check if username exists  
        try:
            username_exists = models.Users.objects.get(username = username)
            authenticated_user = authenticate(username = username, password = password)
            print(authenticated_user)

            if authenticated_user is not None:
                login(request, authenticated_user)
                return HttpResponseRedirect(reverse("task_app:index"))
            
            context = {"message":"Invalid credentials"}
            return render(request, "login.html", context=context)
            
            
        except models.Users.DoesNotExist:
            context = {"message":"User Does not exist"}
            return render(request, "login.html", context=context)
@csrf_exempt
def validate_username(request):
    username = request.POST.get("username")
    # print(username)
    try:
        username_exists = models.Users.objects.get(username = username)
        data = {"r":20}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
    except models.Users.DoesNotExist:
        data = {"r":200}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
@csrf_exempt
def validate_email(request):
    email = request.POST.get("email")
    try:
        email_exists = models.Users.objects.get(email = email)
        data = {"r":20}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
    except models.Users.DoesNotExist:
        data = {"r":200}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

@csrf_exempt
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        print(username, email, password)
        
        try:
            user_exists = User.objects.get(username=username)
            context = {"message": "Username taken!"}
            return render(request, "register.html", context=context)
        except User.DoesNotExist:
            try:
                email_exists = User.objects.get(email=email)
                context = {"message": "Email taken!"}
                return render(request, "register.html", context=context)
            except User.DoesNotExist:
                if password != cpassword:
                    context = {"message": "Passwords do not match!"}
                    return render(request, "register.html", context=context)
                
                user = User(username=username, email=email)
                user.set_password(password)  # Set the hashed password
                user.save()
                context = {"message_success": "User Created Successfully!"}
                return render(request, "register.html", context=context)

         
        
        
        
        
        
         
        


        
    

    




