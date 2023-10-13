from django.urls import path 
from . import views

app_name = "task_app"

urlpatterns = [
    path("", views.index, name = "index"),
    path("create_task/", views.create_task, name = "create_task"),
    path("update_task/", views.update_task, name = "update_task"),
    path("delete_task/", views.delete_task, name = "delete_task"),
    path("login_view/", views.login_view, name = "login_view"),
    path("validate_username/", views.validate_username, name = "validate_username"),
    path("validate_email/", views.validate_email, name = "validate_email"),
    path("register_view/", views.register_view, name = "register_view"),
    path("verify_otp/", views.verify_otp, name = "verify_otp"),
    path("logout_view", views.logout_view, name = "logout_view"),
    path("resend_otp/", views.resend_otp, name = "resend_otp"),
    path("completed/", views.completed_tasks, name = "completed"),
    path("complete_task/", views.complete_task, name = "complete_task")
]
