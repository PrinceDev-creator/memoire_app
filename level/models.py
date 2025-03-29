import random
from django.db import models
# from edutrack.students.models import Student
# from edutrack.subject.models import Subject

class Level(models.Model):
    name=models.CharField(max_length=255)
    group=models.CharField(max_length=10, null=True)
    series=models.CharField(max_length=5, null=True)
    academy=models.ForeignKey('users.Academy', on_delete=models.CASCADE, related_name='levels', default=None)
    effective=models.IntegerField(default=random.randint(10,50))
    # leader1=models.ForeignKey('students.Student', on_delete=models.CASCADE, null=True, blank=True, related_name='leader1')
    # leader2=models.ForeignKey('students.Student', on_delete=models.CASCADE, null=True, blank=True, related_name='leader2')
    # leader3=models.ForeignKey('students.Student', on_delete=models.CASCADE, null=True, blank=True, related_name='leader3')
    # objects : models.Manager['Level']

    def __str__(self):
        return self.name

    # @staticmethod
    # def list_students():
    #     nbr_students = Student.objects.all()
    #     return nbr_students
    #
    # @staticmethod
    # def effective():
    #     nbr_students = Student.objects.count()
    #     return nbr_students
    #
    # @staticmethod
    # def list_subjects():
    #     list_subjects = Subject.objects.all()
    #     return list_subjects
    #
    # @staticmethod
    # def nbr_subjects():
    #     nbr_subjects = Subject.objects.count()
    #     return nbr_subjects
    #
    # @staticmethod
    # def insert_class_leader(level_id, leader1, leader2, leader3):
    #     level = Level.objects.get(pk=level_id)
    #     level.leader1 = leader1,
    #     level.leader2 = leader2,
    #     level.leader3 = leader3
    #     level.save()
    #
    # @staticmethod
    # def leaders_name(level_id):
    #     level = Level.objects.get(pk=level_id)
    #     leaders={
    #         'leader1': Student.objects.get(pk=level.leader1).name,
    #         'leader2': Student.objects.get(pk=level.leader2).name,
    #         'leader3': Student.objects.get(pk=level.leader3).name,
    #     }
    #     return leaders

