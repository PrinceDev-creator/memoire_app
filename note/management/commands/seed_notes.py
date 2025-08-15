import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from note.models import Note
from students.models import Student
# from subject.models import Subject
# from students.models import Student
# from level.models import Level
from animation.models import Animation
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Seed the database with random notes'

    def handle(self, *args, **kwargs):
        num_notes = 50  # Nombre de notes à générer
        
        # subjects = list(Subject.objects.filter(id__range=(1, 11)).order_by("?"))
        # subjects = Subject.objects.all()
        # students = Student.objects.all()
        # levels = Level.objects.all()
        
        animations=Animation.objects.all()
        students =Student.objects.all()
        notes = []
        
        
        
        # if not subjects or not students or not levels:
        #     self.stdout.write(self.style.ERROR('Assurez-vous que les données Subject, Student et Level existent.'))
        #     return
        
        for _ in range(num_notes):
            note = Note(
                score=self.definy_score(),
                student=random.choice(students),
                animation=random.choice(animations),
                cycle=random.randint(1,3),
                created_at=now(),
                updated_at=now()
            )
            notes.append(note)
        
        Note.objects.bulk_create(notes)
        self.stdout.write(self.style.SUCCESS(f'{num_notes} notes insérées avec succès.'))

    def definy_score(self):
        compos = ['Interrogation 1', 'Devoir 1','Interrogation 2', 'Devoir 2', 'Interrogation 3']
        score=Decimal(random.uniform(0, 20)).quantize(Decimal('0.01'))
        compo=random.choice(compos)
        note={
            '{compo}': score,
        }
        return note
    