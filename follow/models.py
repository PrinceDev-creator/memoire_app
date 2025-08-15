from django.db import models
from django.conf import settings

class Follow(models.Model):
    student=models.ForeignKey('students.Student', related_name='students_followed', on_delete=models.CASCADE, null=True, default=None)
    tutor=models.ForeignKey('tutor.Tutor', related_name='tutors_followed', on_delete=models.CASCADE, null=True, default=None)
    level=models.ForeignKey('level.Level', related_name='levels_followed', on_delete=models.CASCADE, null=True, default=None)
    registration_number=models.IntegerField(default=None, null=True)
    academic_year=models.CharField(max_length=10, default=settings.ACADEMIC_YEAR)
    
    class Meta :
        constraints=[models.UniqueConstraint(
            fields=['student', 'tutor', 'academic_year', 'registration_number'],
            name='unique_follow'
        )]

    def __str__(self):
        return self.student
    
    def assign_level_and_year(self, level):
        self.level = level
        self.save()