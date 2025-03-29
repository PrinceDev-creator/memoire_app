from django.db import models

class Participation(models.Model):
    course=models.ForeignKey('animation.Animation', on_delete=models.CASCADE)
    student=models.ForeignKey('students.Student', on_delete=models.CASCADE)
    presence=models.BooleanField()
    note_participation=models.FloatField()
    objects: models.Manager['Participation']