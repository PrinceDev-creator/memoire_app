import json
import string
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.utils import lowercase_first_letter

User=get_user_model()

fake=Faker()


while True:
    try:
        nbr_tutors=int(input("Veuillez entrer le nombre de parent/tuteur à créer : "))
        if nbr_tutors > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")

class Command(BaseCommand) :
    def handle(self, *args, **options):
        
        users_dict=[]
        
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
        
        for i in range(nbr_tutors):
           
           
            email=f"{lowercase_first_letter(fake.first_name())}{fake.email()}"
                
            while User.objects.filter(email=email).exists():
                    email=f"{lowercase_first_letter(fake.first_name())}@gmail.com"
            
            password='123456$Aa'
            
            users_dict.append({
                "email" : email,
                "password": password ,
                "first_name": fake.first_name(),
                "last_name": random.choice(noms_fon),
                "type_user" : "tutor",
                "phone_number": fake.phone_number(),
                "address": fake.address(),
            })
            
        file_path="infos_tutors.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_dict,f,indent=4,ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f"{nbr_tutors} posts de parent/tuteur créés avec succès !"))