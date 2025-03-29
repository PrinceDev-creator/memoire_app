import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from note.models import Note
from subject.models import Subject
from students.models import Student
from level.models import Level
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Seed the database with random notes'

    def handle(self, *args, **kwargs):
        num_notes = 50  # Nombre de notes à générer
        
        subjects = list(Subject.objects.filter(id__range=(1, 11)).order_by("?"))
        students = list(Student.objects.filter(id__range=(21, 40)).order_by("?"))
        levels = list(Level.objects.filter(id__range=(1, 15)).order_by("?"))
        
        if not subjects or not students or not levels:
            self.stdout.write(self.style.ERROR('Assurez-vous que les données Subject, Student et Level existent.'))
            return
        
        notes = []
        for _ in range(num_notes):
            note = Note(
                score=Decimal(random.uniform(0, 20)).quantize(Decimal('0.01')),
                subject=random.choice(subjects),
                quiz=random.randint(1, 5),
                cycle=random.randint(1,3),
                student=random.choice(students),
                level=random.choice(levels),
                created_at=now(),
                updated_at=now()
            )
            notes.append(note)
        
        Note.objects.bulk_create(notes)
        self.stdout.write(self.style.SUCCESS(f'{num_notes} notes insérées avec succès.'))
