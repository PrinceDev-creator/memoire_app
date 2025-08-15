from django.db import models

from django.contrib.auth import get_user_model

User=get_user_model()

class Tutor(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutors_spec', default=None, null=True)
    first_name=models.CharField(max_length=100, default='not defined', null=True)
    last_name=models.CharField(max_length=100,default='not defined', null=True) 
    phone_number=models.CharField(max_length=20, default='not defined', null=True)
    email=models.EmailField(max_length=100, default='not defined', null=True)
    address=models.CharField(max_length=255, default='not defined', null=True)
    # connexion_key=models.CharField(max_length=100,null=True)

    
    def __str__(self):
        return self.first_name
