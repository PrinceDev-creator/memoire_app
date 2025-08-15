import json
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

nbr_notes=input("Entrer le nombre de classe que vous désirer créer: ")
while True:
    try:
        nbr_notes=int(nbr_notes)
        if nbr_notes > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")
nbr_notes=int(nbr_notes)


class Command(BaseCommand):
    help = 'Seed the database with random notes'

    def handle(self, *args, **kwargs):
        # num_notes = 50  # Nombre de notes à générer
        
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
        
        for _ in range(nbr_notes):
            note = Note(
                score=self.definy_score(),
                student=random.choice(students),
                animation=random.choice(animations),
                cycle=random.randint(1,3),
                created_at=now(),
                updated_at=now()
            )
            notes.append(note)
            
        self.write_in_file(notes)
        
        self.stdout.write(self.style.SUCCESS(f'{nbr_notes} post de notes créées avec succès.'))

    def definy_score(self):
        compos = ['Interrogation 1', 'Devoir 1','Interrogation 2', 'Devoir 2', 'Interrogation 3']
        score=Decimal(random.uniform(0, 20)).quantize(Decimal('0.01'))
        compo=random.choice(compos)
        note={
            compo: float(score),
        }
        return note
    
    def write_in_file(self, notes):
        file_path = "post_notes.json"
        notes_data = [self.to_dict(note) for note in notes]  # Convertit chaque Note en dict
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(notes_data, f, indent=4, ensure_ascii=False)
                
    def to_dict(self,note):
        return {
            'score': str(note.score),  # Convertit Decimal en string pour JSON
            'student': note.student.id,
            'animation': note.animation.id,
            'cycle': note.cycle,
            'created_at': note.created_at.isoformat(),
            'updated_at': note.updated_at.isoformat()
        }