import random
from django.core.management.base import BaseCommand
from school.models import School
from subject.models import Subject  # Remplacez 'your_app' par le nom de votre application

class Command(BaseCommand):
    help = 'Seed the Subject model with unique sample data'

    def handle(self, *args, **kwargs):
        # Récupérer toutes les écoles existantes
        schools = School.objects.all()
        
        if not schools.exists():
            self.stdout.write(self.style.ERROR('Aucune école trouvée. Veuillez créer des écoles d\'abord.'))
            return

        # Liste des matières possibles avec leurs catégories
        SUBJECTS_DATA = [
            # Sciences
            {'name': 'Mathématiques', 'category': 'SCIENCE'},
            {'name': 'Physique', 'category': 'SCIENCE'},
            {'name': 'Chimie', 'category': 'SCIENCE'},
            {'name': 'Biologie', 'category': 'SCIENCE'},
            {'name': 'SVT', 'category': 'SCIENCE'},
            
            # Littérature
            {'name': 'Français', 'category': 'LITERATURE'},
            {'name': 'Anglais', 'category': 'LITERATURE'},
            {'name': 'Espagnol', 'category': 'LITERATURE'},
            {'name': 'Philosophie', 'category': 'LITERATURE'},
            
            # Informatique
            {'name': 'Algorithmique', 'category': 'COMPUTER_SCIENCE'},
            {'name': 'Programmation', 'category': 'COMPUTER_SCIENCE'},
            {'name': 'Réseaux', 'category': 'COMPUTER_SCIENCE'},
            
            # Arts
            {'name': 'Musique', 'category': 'ART'},
            {'name': 'Arts plastiques', 'category': 'ART'},
            {'name': 'Théâtre', 'category': 'ART'},
            
            # Autres
            {'name': 'Histoire-Géographie', 'category': 'OTHER'},
            {'name': 'EPS', 'category': 'OTHER'},
            {'name': 'Education civique', 'category': 'OTHER'},
        ]

        # Vérifier les matières existantes pour éviter les doublons
        existing_subjects = set(Subject.objects.values_list('name', flat=True))
        new_subjects = []

        for subject_data in SUBJECTS_DATA:
            if subject_data['name'] not in existing_subjects:
                new_subjects.append(Subject(
                    name=subject_data['name'],
                    category=subject_data['category'],
                    school=random.choice(schools)
                 )
                )
                existing_subjects.add(subject_data['name'])  # Ajouter à l'ensemble pour éviter les doublons dans cette session

        # Création en masse pour optimiser les performances
        if new_subjects:
            Subject.objects.bulk_create(new_subjects)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(new_subjects)} new unique subjects'))
        else:
            self.stdout.write(self.style.WARNING('All subjects already exist in database'))
