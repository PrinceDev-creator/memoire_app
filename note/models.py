from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from ..students.models import Student
# from ..subject.models import  Subject
# from ..level.models import  Level
# from ..users.models import Teacher

class Note(models.Model):
    quiz = models.JSONField(null=True, blank=True)  # Stocker les évaluations et leurs notes sous forme de dictionnaire
    exam = models.JSONField(null=True, blank=True)  # Stocker les évaluations et leurs notes sous forme de dictionnaire
    cycle = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='notes_student')
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE, related_name='notes_subject')
    level = models.ForeignKey('level.Level', on_delete=models.CASCADE, related_name='notes_level')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects: models.Manager["Note"]
    
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['student','level','subject','cycle','quiz'],
                name='unique_note'
                
            )
        ]

    # def display_note(self):
    #     return {
    #         'student' : Student.objects.get(pk=self.student).name,
    #         'level' : Level.objects.get(pk=self.level).name,
    #         'subject': Subject.objects.get(pk=self.subject).name,
    #         'teacher':Teacher.objects.get(pk=self.teacher).name,
    #         'note': self.note,
    #         'quiz': self.quiz,
    #         'semester': self.cycle,
    #         'created_at':self.created_at,
    #         'updated_at':self.updated_at,
    #     }
    #
    # def set_note(self, note, quiz,cycle, teacher, student, subject):
    #     self.note=note
    #     self.subject=subject
    #     self.quiz=quiz
    #     self.cycle=cycle
    #     self.teacher=teacher
    #     self.student=student
    #     self.save()



