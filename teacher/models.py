from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

class Teacher(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_spec', null=True)
    first_name=models.CharField(max_length=100, default='not defined', null=True)
    last_name=models.CharField(max_length=100,default='not defined', null=True)
    # school=models.ForeignKey('school.school',on_delete=models.CASCADE, related_name='teachers_school_spec', default=None, null=True)
    #starting_year_in_academy=models.DateField(null=True)
    title=models.CharField(max_length=100, null=True, blank=True, default='not defined')
    phone_number=models.CharField(max_length=20, default='not defined', null=True)

    def __str__(self):
        return self.first_name