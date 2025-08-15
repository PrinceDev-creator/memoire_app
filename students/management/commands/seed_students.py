import random
import json
import string
from django.core.management.base import BaseCommand
from faker import Faker
from school.models import School
from ...models import Student
from level.models import Level

fake = Faker()

nbr_student=input("Entrer le nombre de classe que vous désirer créer: ")
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
    help = "Générer des étudiants fictifs"

    def handle(self, *args, **kwargs):
        students = []
        schools = School.objects.all()  # Academy définie
        levels=Level.objects.all()  # Academy définie
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
        for _ in range(nbr_student):  # Générer 20 étudiants
            first_name=fake.first_name()
            last_name=random.choice(noms_fon)
            registration_number = random.randint(100000, 999999)  # Numéro unique
            school = random.choice(schools)  # École aléatoire
            level = random.choice(levels)  # Niveau entre 1 et 15
            year_academy = random.randint(2020, 2024)  # Année aléatoire
            student_key=self.generate_student_key_key()
            # tutor=Tutor.objects.filter(id__range=(76,90)).order_by("?").first()
            
            student = Student(
                first_name=first_name,
                last_name=last_name,
                school=school,
                registration_number=registration_number,
                level=level,
                year_academy=year_academy,
                student_key=student_key,
                sexe=random.choice(['M', 'F']),  # Sexe aléatoire
                  # Peut être None
            )
            students.append(student)

        # Enregistrement en base
        Student.objects.bulk_create(students)
        
        self.stdout.write(self.style.SUCCESS(f"{len(students)} étudiants créés avec succès !"))
        
    def generate_student_key_key(self):
        student_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        while Student.objects.filter(student_key=student_key).exists():
            student_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        print(student_key)
        return student_key
    
    def generate_registration_number(self):
        registration_number = random.randint(100000, 999999) 
        while Student.objects.filter(registration_number=registration_number).exists():
            registration_number = random.randint(100000, 999999)
        return registration_number
        
    
        
        
        