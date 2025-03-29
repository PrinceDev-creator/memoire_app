from django.db import models
import random
import string

class Animation(models.Model):
    subject=models.ForeignKey('subject.Subject', on_delete=models.CASCADE)
    level=models.ForeignKey('level.Level', on_delete=models.CASCADE)
    teacher=models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    student=models.ForeignKey('students.Student', on_delete=models.CASCADE)
    coefficient=models.IntegerField()
    teacher_key = models.CharField(max_length=10, unique=True, editable=False)

    def generate__key(self):
        """Génère une clé unique de 10 caractères alphanumériques."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def save(self, *args, **kwargs):
        """Surcharge la méthode save pour générer un teacher_key unique."""
        if not self.teacher_key:  # Générer un teacher_key uniquement si non défini
            self.teacher_key = self.generate_teacher_key()
            while Animation.objects.filter(teacher_key=self.teacher_key).exists():
                self.teacher_key = self.generate_teacher_key()
        super().save(*args, **kwargs)

    
    