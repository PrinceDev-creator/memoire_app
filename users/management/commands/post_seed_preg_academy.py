import json
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.utils import lowercase_first_letter

User=get_user_model()

fake=Faker()


while True:
    try:
        nbr_academies=int(input("Veuillez entrer le nombre d'école à créer : "))
        if nbr_academies > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")


class Command(BaseCommand):
    
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
        
        benin_addresses = [
    "Rue 2618, Haie Vive, Cotonou, Bénin",
    "Avenue Steinmetz, Cotonou, Bénin",
    "Quartier Zongo, Porto-Novo, Bénin",
    "Boulevard de la Marina, Cotonou, Bénin",
    "Place de l'Étoile Rouge, Cotonou, Bénin",
    "Ganhi, Centre-ville, Cotonou, Bénin",
    "Avenue Clozel, Porto-Novo, Bénin",
    "Rue des Banques, Abomey-Calavi, Bénin"
]
    
        
        
        for i in range(nbr_academies):
            
            initial_academy=['Complexe scolaire', 'CEG', 'Lycée']
            first_name=fake.first_name()
            director=f"{random.choice(noms_fon)} {first_name}"
            place=random.choice(benin_addresses)
            academy=f"{random.choice(initial_academy)} {fake.name()}"
            password='123456$Aa'
            email=f"{lowercase_first_letter(first_name)}{fake.email()}"
            while User.objects.filter(email=email).exists():
                email=f"{lowercase_first_letter(first_name)}{fake.email()}" 
            
            
            users_dict.append({
                "email": email,
                "school_name": academy,
                "password" : password,
                "director": director,
                "address": place,
                "phone_number": fake.phone_number(),
             }
            )
            
        
        file_path="infos_preg_academy.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_dict,f,indent=4,ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f"{nbr_academies} posts d'école créés avec succès !"))