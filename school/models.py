from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class School(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='schools', default=None)
    school_name= models.CharField(max_length=100, default='not defined', null=False)
    address=models.CharField(max_length=128,default='', null=False)
    director=models.CharField(max_length=100,default='', null=False)
    phone_number=models.CharField(max_length=20, default='not defined', null=True)
    email=models.EmailField(max_length=100, default='not defined', null=True)
    
    def __str__(self):
        return self.school_name   

