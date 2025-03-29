import json
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import Tutor, UserApp

fake = Faker()


# print("-----Début de suppression des tuteurs----")

# for i in range(15):
#     last_user=Tutor.objects.last()
#     if last_user:
#         last_user.delete()
#         print(f"Suppression {i}")
#     else :
#         print("Aucun tuteur trouvé")

# print("-----Début de suppression des utilisateurs----")

# for i in range(15):
#     last_user=UserApp.objects.last()
#     if last_user:
#         last_user.delete()
#         print(f"Suppression {i}")
#     else :
#         print("Aucun utilisateur trouvé")

# print("-----Fin des suppressions-----")

class Command(BaseCommand):
    help = "Générer des utilisateurs et des tuteurs fictifs"

    def handle(self, *args, **kwargs):
        users = []
        tutors = []
        
        for _ in range(15): 
            email = f"{fake.email()}_{random.randint(1000, 9999)}"
            
            while UserApp.objects.filter(email=email).exists():
                email = f"{fake.email()}_{random.randint(1000, 9999)}"

            user = UserApp(
                email=fake.email(),
                is_tutor=True
            )
            password = "tutorPassword"
            user.set_password(password)

            tutor = Tutor(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                active=random.choice([True, False]),
            )
            tutors.append(tutor)
            users.append(user)

        UserApp.objects.bulk_create(users)
        Tutor.objects.bulk_create(tutors)

        # Sauvegarder les infos des utilisateurs dans un fichier JSON
        # file_path = "infos_tutors.json"
        # with open(file_path, "w", encoding="utf-8") as f:
        #     json.dump(users, f, indent=4, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(f"{len(tutors)} tuteurs créés avec succès !"))
