from django.db import models

class Student(models.Model):
    first_name= models.CharField(max_length=255, default='not defined')
    last_name= models.CharField(max_length=255, default='not defined')
    school =models.ForeignKey('school.School', on_delete=models.CASCADE, related_name='students', default=None, null=True)
    registration_number=models.IntegerField(default=None, null=True, unique=True)
    # level=models.ForeignKey('level.Level', on_delete=models.CASCADE, related_name='students_level',default=None)
    # year_of_arrival =models.IntegerField(null=True)
    student_key=models.CharField(max_length=100, null=True, unique=True)
    sexe=models.CharField(max_length=1, default="M")
    registration_number=models.CharField(max_length=20, unique=True, null=True, blank=True)
    # tutor=models.ForeignKey('users.Tutor', blank=True, null=True, on_delete=models.CASCADE,related_name='children')
    
    
    class Meta:
        constraints=[
            models.UniqueConstraint(
                name='unique_student_key_registration_number',
                fields=['student_key', 'registration_number']
            )
        ]
    
    def __str__(self):
        return self.first_name