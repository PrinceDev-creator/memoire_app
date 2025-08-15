import string
import random
from faker import Faker
from level.models import Level
from subject.models import Subject
from users.models import Teacher, Academy
from django.core.exceptions import ObjectDoesNotExist

def generate_teacher_key():
    return ''.join(random.choices(string.digits, k=6))

def detect_duplicate_teacher_key(teacher_key):
    while Teacher.objects.filter(teacher_key=teacher_key).exists():
        teacher_key = ''.join(random.choices(string.digits, k=6))   
    return teacher_key

def seed_teachers(academy_id):
    if not isinstance(academy_id, int):
        raise ValueError("academy_id doit être un entier valide.")

    try:
        academy = Academy.objects.get(pk=academy_id)  # Récupérer un seul objet
    except ObjectDoesNotExist:
        raise ValueError(f"Aucune académie trouvée avec l'ID {academy_id}")

    levels = Level.objects.filter(academy_id=academy_id)
    subjects = Subject.objects.filter(academy_id=academy_id)

    if not levels.exists() or not subjects.exists():
        raise ValueError(f"Pas de niveaux ou de matières trouvés pour l'académie {academy_id}")

    all_trio_of_academy_level_subject = [(academy, level, subject) for level in levels for subject in subjects]
    random.shuffle(all_trio_of_academy_level_subject)

    teachers=[]

    for academy, level, subject in all_trio_of_academy_level_subject:
        try:
            teacher_key = detect_duplicate_teacher_key(generate_teacher_key())
            print(teacher_key, academy, level, subject)
            
            # Vérifier que les objets sont bien des instances de leur modèle
            if not isinstance(level, Level) or not isinstance(subject, Subject):
                raise ValueError("Level ou Subject est invalide.")

            teacher=Teacher(
                teacher_key=teacher_key,
                level=level,
                subject=subject,
                academy=academy
            )
            
            teachers.append(teacher)

        except Exception as e:
            raise Exception(f"Une erreur s'est produite : {e}")
    
    Teacher.objects.bulk_create(teachers)
