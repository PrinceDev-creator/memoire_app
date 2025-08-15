from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from subject.models import Subject
from django.apps import apps
# from edutrack.main import Subject
# from students.models import Student
#
# Subject=apps.get_model('subject','Subject')
# Student=apps.get_model('students', 'Student')
# Level = apps.get_model('level', 'Level')
# # Note = apps.get_model('note', 'Note')

class UserApp(AbstractUser):
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    username=models.CharField(null=True)
    email=models.EmailField(null=False, default="not defined")
    password=models.CharField(default='not defined', null=True)
    is_academy= models.BooleanField(default=False)
    is_teacher= models.BooleanField(default=False)
    is_tutor= models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    connexion_key=models.CharField(null=True)
    # teacher=models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='users-teacher', null=True, to_field='Teacher.teacher_key')
    # tutor=models.ForeignKey('users.Tutor', on_delete=models.CASCADE, related_name='users-tutor', null=True, to_field='Tutor.student_key')
    # # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    # class Meta:
    #     constraints=[
    #         models.UniqueConstraint(
    #             fields=['user_key'],
    #             name='unique_user_key'
    #         )
    #     ]
            
    
    # groups = models.ManyToManyField(
    #     'auth.Group', related_name='users', blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission', related_name='users', blank=True
    # )
    
    class Meta:
        verbose_name='Utilisateur'
        verbose_name_plural='Utilisateurs'     

class Academy(models.Model):
    user=models.OneToOneField(UserApp, on_delete=models.CASCADE, related_name='academies', default=None)
    academy= models.CharField(max_length=100, default='not defined', null=False)
    place=models.CharField(max_length=128,default='', null=False)
    director=models.CharField(max_length=100,default='', null=False)
    
    def __str__(self):
        return self.academy 

  

class Teacher(models.Model):
    user=models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='teachers', null=True)
    first_name=models.CharField(max_length=100, default='not defined', null=True)
    last_name=models.CharField(max_length=100,default='not defined', null=True)
    academy=models.ForeignKey('school.School',on_delete=models.CASCADE, related_name='teachers_academy')
    level=models.ForeignKey('level.Level', on_delete=models.CASCADE,related_name='teachers_level', null=True)
    subject=models.ForeignKey('subject.Subject',on_delete=models.CASCADE, related_name='teachers_subject', null=True)
    coefficient=models.IntegerField(null=True, blank=True, default=None)
    starting_year_in_academy=models.DateField(null=True)
    title=models.CharField(max_length=100, null=True, blank=True, default='not defined')
    level_key=models.CharField(max_length=100,null=True)
    
    # class Meta:
    #     constraints=[
    #         models.UniqueConstraint(
    #             fields=['academy','level','subject', 'coefficient', 'level_key'],
    #             name='unique_level_key_per_academy_per_subject_per_level_per_coefficient'
    #         )
    #     ]
     
    def __str__(self):
        return self.first_name

class Tutor(models.Model):
    user=models.ForeignKey(UserApp, on_delete=models.CASCADE, related_name='tutors', default=None, null=True)
    first_name=models.CharField(max_length=100, default='not defined', null=True)
    last_name=models.CharField(max_length=100,default='not defined', null=True) 
    list_student_key=models.JSONField(default=list)
    connexion_key=models.CharField(max_length=100,null=True)

    
    def __str__(self):
        return self.first_name