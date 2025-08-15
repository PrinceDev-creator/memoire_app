import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from animation.models import Animation
from subject.models import Subject
from teacher.models import Teacher
from level.models import Level

User=get_user_model()

nbr_animations=input("Entrer le nombre d'animations que vous désirer créer: ")
while True:
    try:
        nbr_student=int(nbr_student)
        if nbr_student > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")
nbr_student=int(nbr_student)



class Command(BaseCommand):
    help = 'Seed the database with random notes'
    animations=[]

    def handle(self, *args, **kwargs):
        num_notes = 50  # Nombre de notes à générer
        
        # subjects = list(Subject.objects.filter(id__range=(1, 11)).order_by("?"))
        subjects = Subject.objects.all()
        levels = Level.objects.all()
        teachers = Teacher.objects.all()
        teacher_keys = []
        
        for teacher in teachers:
            user=teacher.user
            teacher_key=user.connexion_key
            teacher_keys.append(teacher_key)

        for _ in range(len(teachers)):
            level=random.choice(levels)
            animation = Animation(
                subject=random.choice(subjects),
                level=level,
                teacher=random.choice(teachers),
                school=level.school,
                coefficient=random.randint(1, 5),
                animation_key=self.generate_connexion_key()
                
            )
            
            if self.can_add_animation(animation.level, animation.subject):
                self.animations.append(animation)
        # Vérifie si la combinaison existe déjà
        
        Animation.objects.bulk_create(self.animations)
        
        self.stdout.write(self.style.SUCCESS(f'{len(self.animations)} créées avec succès.'))


    def can_add_animation(self, level, subject):
        return not any(
            anim.level == level and anim.subject==subject
            for anim in self.animations
        )
            
    def generate_connexion_key(self):
        animation_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        for animation in self.animations:
            while animation.animation_key==animation_key:
                animation_key=''.join(random.choices(string.ascii_letters + string.digits, k=10)) 
        
        print(animation_key)
        return animation_key