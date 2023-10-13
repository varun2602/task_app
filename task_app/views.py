from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail 
from django.conf import Settings
from django.utils import timezone
import json
from . import models
import random

otp = []

@login_required(login_url="http://127.0.0.1:8000/login_view/")
def index(request):
    tasks_all = models.Task.objects.filter(user = request.user, is_active = True).order_by("task_name")
    context = {"user":request.user, "verification":request.user.is_verified, "all_tasks":tasks_all}
    return render(request, "index.html", context)

@csrf_exempt
def create_task(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        user = models.Users.objects.get(username = user_name)
        task_to_add = request.POST.get("task_to_add")
        # Check if the task already exists 
        if models.Task.objects.filter(task_name = task_to_add).exists():
            data = {"add_task":20}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = "application/json")

        task = models.Task.objects.create(task_name = task_to_add, user = user )
        task.save()
        data = {"add_task":200}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
def completed_tasks(request):
    if models.Task.objects.filter(is_active = False).exists():
        completed_tasks = models.Task.objects.filter(is_active = False)
        context = {"completed_tasks":completed_tasks}
        return render(request, "completed.html", context)

    return render(request, "completed.html")

@csrf_exempt
def complete_task(request):
    if request.method == "POST":
        task_name = request.POST.get("task_name")
        task_model = models.Task.objects.get(task_name = task_name)
        task_model.is_active = False 
        task_model.save()
        data = {"completed_task":200}
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")


@csrf_exempt
def update_task(request):
    if request.method == "POST":
        current_task_name = request.POST.get("current_task")
        updated_task_name = request.POST.get("updated_task")
        update_task_model = models.Task.objects.get(task_name = current_task_name)
        # print(update_task_model.task_name)
        update_task_model.task_name = updated_task_name
        update_task_model.save()
        data = {"update_response":200} 
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
@csrf_exempt
def delete_task(request):
    if request.method == "POST":
        task_name = request.POST.get("task_name")
        task_to_delete = models.Task.objects.filter(task_name = task_name)
        for task in task_to_delete:
            task.delete()
        data = {"delete_response":200} 
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")
    
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
    
@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        otp = int(request.POST.get("otp"))
        user = request.POST.get("user")

        user_check_otp = models.Users.objects.get(username = user)
        otp_check_model = models.otp_verification.objects.get(user = user_check_otp)
       
    #    Checking time difference  
        current_time = timezone.now()
        created_at = otp_check_model.created_at 
        time_difference = current_time - created_at
        hours_difference = time_difference.total_seconds()/3600
        if hours_difference > 1:
            otp_check_model.delete()
            data = {"otp_response":20}
        
        if otp == otp_check_model.otp_number:
            user_check_otp.is_verified = True
            user_check_otp.save()
            data = {
                "otp_response":200
            }
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = "application/json")
            
        
        data = {
            "otp_response":20
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type = "application/json")

        




@csrf_exempt
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        
        # Check if the username is already taken
        if models.Users.objects.filter(username=username).exists():
            context = {"message": "Username taken!"}
            # return render(request, "register.html", context=context)
            json_data = json.dumps(context)
            return HttpResponse(json_data, content_type = "application/json")

        # Check if the email is already taken
        if models.Users.objects.filter(email=email).exists():
            context = {"message": "Email taken!"}
            # return render(request, "register.html", context=context)
            json_data = json.dumps(context)
            return HttpResponse(json_data, content_type = "application/json")

        # Check if passwords match
        if password != cpassword:
            context = {"message": "Passwords do not match!"}
            # return render(request, "register.html", context=context)
            json_data = json.dumps(context)
            return HttpResponse(json_data, content_type = "application/json") 
            
        
        # Create a new user and hash the password
        user = models.Users.objects.create_user(username, email, password)
        user.set_password(password)
        user.save()
        user_for_otp = models.Users.objects.get(username = username)

        # Generate and store OTP
        otp_number = random.randint(1000, 9999)
        otp_instance = models.otp_verification(otp_number=otp_number, user=user_for_otp)
        otp_instance.save()

        # Send OTP via email
        send_mail(
            subject='OTP for verification',
            message=f'Your one-time verification OTP is {otp_number}. OTP will be valid only for 1 hour',
            from_email='cosmosv26@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        context = {"message_success":"Registered successfully! Verify your account with email otp. Otp will be valid for 1 hour"}
        json_data_success = json.dumps(context)
        return HttpResponse(json_data_success, content_type = "application/json")
        # return HttpResponseRedirect(reverse("index"))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("task_app:index"))

@csrf_exempt
def resend_otp(request):
    if request.method == "POST":
        otp_number = random.randrange(1000, 10000)
        user = request.POST.get("user")
        user_to_verify = models.Users.objects.get(username = user)
        email = user_to_verify.email
        print(user_to_verify.username)
        try:
            otp_model_exists = models.otp_verification.objects.get(user = user_to_verify)
            otp_model_exists.otp_number = otp_number
            otp_model_exists.created_at = timezone.now()
            otp_model_exists.save()
            send_mail(
            subject='OTP for verification',
            message=f'Your one-time verification OTP is {otp_number}. OTP will be valid only for 1 hour',
            from_email='cosmosv26@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
            data = {"otp_resend":200}
            json_data =  json.dumps(data)

            return HttpResponse(json_data, content_type = "application/json")
        except models.otp_verification.DoesNotExist:
            otp_model_new = models.otp_verification.objects.create(user = user_to_verify, otp_number = otp_number)
            otp_model_new.save()
            send_mail(
            subject='OTP for verification',
            message=f'Your one-time verification OTP is {otp_number}. OTP will be valid only for 1 hour',
            from_email='cosmosv26@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
            data = {"otp_resend":200}
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type = "application/json")


        
               

         
        
        
        
        
        
         
        


        
    

    




