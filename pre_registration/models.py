from django.db import models

class PreRegistration(models.Model):
    school_name= models.CharField(max_length=100, default='not defined', null=False)
    director=models.CharField(max_length=100,default='', null=False)
    email=models.EmailField(max_length=100, default='not defined', null=True)
    phone_number=models.CharField(max_length=20, default='not defined', null=True)
    address=models.CharField(max_length=255, default='not defined', null=True)
    # password=models.CharField(max_length=100, default='not defined', null=True)
    state=models.BooleanField(default=None, null=True)
    
    def __str__(self):
        return self.school_name   

