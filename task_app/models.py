from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    email = models.EmailField(max_length = 50, blank = True, null = True, unique=True) 
    is_verified = models.BooleanField(default = False)
    # user = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="user_task")

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]
    # groups = models.ManyToManyField(
    #     'auth.Group', related_name='custom_user_groups', blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission', related_name='custom_user_permissions', blank=True
    # )
    def __str__(self):
        return self.username

# class UsersUnverified(models.Model):
#     email = models.EmailField(max_length = 50, blank = True, null = True, unique=True) 
#     username = models.CharField(max_length = 50, blank = True, null = True)
#     password = models.CharField(max_length = 50, blank = True, null = True)

#     def __str__(self):
#         return self.username

class Task(models.Model):
    task_name = models.CharField(max_length = 100, blank = True, null = True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(Users, blank = True, null = True,  on_delete= models.CASCADE, related_name="user_task")
    

    def __str__(self):
        return f"{self.task_name} of {self.user}"

class otp_verification(models.Model):
    otp_number = models.IntegerField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.otp_number} for {self.user} created at {self.created_at}"
    