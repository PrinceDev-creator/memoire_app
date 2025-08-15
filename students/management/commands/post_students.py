import random
import json
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import Academy, Tutor
from ...models import Student
from level.models import Level
from follow.models import Follow

fake = Faker()

nbr_students=input("Entrer le nombre de post que vous désirer créer: ")

nbr_students=int(nbr_students)

class Command(BaseCommand):
    help = "Générer des étudiants fictifs"

    def handle(self, *args, **kwargs):
        students = []
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
        
        
        for _ in range(nbr_students):  # Générer 20 étudiants
            first_name=fake.first_name()
            last_name=random.choice(noms_fon)
            registration_number = self.generate_registration_number()  # Numéro unique
            # year_of_arrival = random.randint(2020, 2024)  # Année aléatoire
            sexe=random.choice(['M', 'F'])# Redoublement max 2 fois
            # tutor=Tutor.objects.filter(id__range=(76,90)).order_by("?").first()
            
            students.append({
                "first_name":first_name,
                "last_name":last_name,
                "registration_number":registration_number,
                "sexe" : sexe
            })

        file_path="post_students.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(students,f,indent=4,ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f"{nbr_students} posts d'apprenants créés avec succès !"))
      
    def generate_registration_number(self):
        registration_number = random.randint(100000, 999999) 
        while Follow.objects.filter(registration_number=registration_number).exists():
            registration_number = random.randint(100000, 999999)
        return registration_number
    