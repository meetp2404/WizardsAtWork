from django.db import models
from datetime import datetime
from .current_user import get_current_user
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class register(models.Model):
    uname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, null=True, blank=True)
    is_created_date = models.DateField(auto_now_add=True)
    is_created_time = models.DateField(auto_now_add=True)

class uploadCar(models.Model):
    User= settings.AUTH_USER_MODEL
    uname = models.ForeignKey(User, null=False,on_delete=models.CASCADE)
    timestamp = datetime.now().strftime('%Y%m%d%H:%M:%S')
    carImage = models.ImageField(upload_to='img/')

class uploadVIN(models.Model):
    User= settings.AUTH_USER_MODEL
    uname = models.ForeignKey(User, null=False,on_delete=models.CASCADE)
    timestamp = datetime.now().strftime('%Y%m%d%H:%M:%S')
    vinImage = models.ImageField(upload_to='imgVIN/')