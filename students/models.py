from django.db import models

class Student(models.Model):
    first_name= models.CharField(max_length=255, default='not defined')
    last_name= models.CharField(max_length=255, default='not defined')
    academy =models.ForeignKey('users.Academy', on_delete=models.CASCADE, related_name='students', default=None)
    registration_number=models.IntegerField()
    level=models.ForeignKey('level.Level', on_delete=models.CASCADE, related_name='students_level',default=None)
    year_academy =models.IntegerField(null=True)
    repeating=models.IntegerField(default=0)
    tutor=models.ForeignKey('users.Tutor', blank=True, null=True, on_delete=models.CASCADE,related_name='children')

    def __str__(self):
        return self.name