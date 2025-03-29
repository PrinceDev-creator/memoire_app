import random
import json
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import Academy, Tutor
from ...models import Student
from level.models import Level

fake = Faker()

class Command(BaseCommand):
    help = "Générer des étudiants fictifs"

    def handle(self, *args, **kwargs):
        students = []
        academy = Academy.objects.get(id=20)  # Academy définie
        noms_fon = [
    "Koffi", "Gnon", "Togbè", "Dossou", "Houssou", "Sêwanou", "Agbo", "Dah", "Tchètchè", "Sossou",
    "Adjovi", "Akpédjé", "Assiba", "Yéyé", "Ganhouan", "Houénou", "Koudjo", "Kpakpo", "Ahossi", "Azongnidé",
    "Noudéhouénou", "Tchalla", "Gbéto", "Adanhoumé", "Agossou", "Tovognan", "Sègbo", "Goudou", "Nononsi", "Houédanou",
    "Azon", "Adjibadé", "Sènou", "Tossou", "Kponton", "Vodounon", "Ahouansou", "Zossou", "Gbaguidi", "Agbessi", 
    "Lokossou", "Hounnongan", "Guézodjè", "Aïkpé", "Aké", "Kodjo", "Ablo", "Hounsa", "Nonvignon", "Houton",
    "Houngbo", "Azon", "Adéchi", "Soglo", "Dovonou", "Zinsou", "Houdé", "Tognissè", "Alladatin", "Houndété",
    "Djidonou", "Gandaho", "Adjagba", "Aïssi", "Gbédji", "Adissin", "Tchobo", "Agonkan", "Dovènon", "Hounguè",
    "Sènadé", "Vodouhè", "Hounkpatin", "Agbokou", "Dossou-Yovo", "Zannou", "Houngnibo", "Gandonou", "Akotégnon", "Alapini",
    "Kponton", "Adjavon", "Houton", "Goudjènou", "Avodagbé", "Kossou", "Assogba", "Noumonvi", "Houtondji", "Dahouénon",
    "Boco", "Kpassidè", "Zon", "Agbohoun", "Gonçalo", "Tossou", "Lokonon", "Houdégbé", "Fadonougbo", "Dogbo"
]
        
        
        for _ in range(20):  # Générer 20 étudiants
            first_name=fake.first_name()
            last_name=random.choice(noms_fon)
            registration_number = random.randint(100000, 999999)  # Numéro unique
            level = Level.objects.get(id=random.randint(1, 15))  # Niveau entre 1 et 15
            year_academy = random.randint(2020, 2024)  # Année aléatoire
            repeating = random.randint(0, 2)  # Redoublement max 2 fois
            tutor=Tutor.objects.filter(id__range=(76,90)).order_by("?").first()
            
            student = Student(
                first_name=first_name,
                last_name=last_name,
                academy=academy,
                registration_number=registration_number,
                level=level,
                year_academy=year_academy,
                repeating=repeating,
                tutor=tutor  # Peut être None
            )
            students.append(student)

        # Enregistrement en base
        Student.objects.bulk_create(students)
        
        self.stdout.write(self.style.SUCCESS(f"{len(students)} étudiants créés avec succès !"))