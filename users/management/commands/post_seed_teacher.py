import json
import string
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from level.models import Level
from subject.models import Subject
from teacher.models import Teacher
from faker import Faker
import random
from datetime import datetime,timedelta
from utils.helps import lowercase_first_letter

fake=Faker()

User=get_user_model()

while True:
    try:
        nbr_teachers=int(input("Veuillez entrer le nombre d'enseignants à créer : "))
        if nbr_teachers > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")


class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        users_dict=[]
        
        levels=Level.objects.all()  # Academy définie
        subjects=Subject.objects.all()
        
        titles=[
            "Professeur titulaire",
            "Professeur vacataire",
            "Conseiller pédagogique",
            "Professeur titulaire et conseiller pédagogique"
        ]
        
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
            
        # num_teachers=5
        # selected_pair=[]

        # all_pair_of_level_subject=[(level, subject) for level in range(levels) for subject in range(subjects)]
        # random.shuffle(all_pair_of_level_subject)

        # for level_id,subject_id in all_pair_of_level_subject:
        #     try:
        #         if (Level.objects.get(id=level_id).DoesNotExist and Subject.objects.get(id=subject_id).DoesNotExist):
        #             selected_pair+=[(level_id,subject_id)]
        #     except IntegrityError: 
        #         print("Cette combinaison de classe/matière existe déjà")
                
        #     if len(selected_pair)==nbr_teachers : break        
        
        # print(selected_pair)    
            
        for _ in range(nbr_teachers):
            
            # if (Level.objects.get(id=level_id).DoesNotExist and Subject.objects.get(id=subject_id).DoesNotExist):
            
            #     # email=f"{lowercase_first_letter(fake.first_name())}{fake.email()}"
            #     email=fake.email()
            #     user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
                
            #     while User.objects.filter(email=email).exists() and User.objects.filter(user_key=user_key).exists():
            #         email=fake.email()
            #         user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    
                
                password='123456$Aa'
                
                
                users_dict.append({
                        # "username": user.username,
                        "email" : "grubfan67@gmail.com",
                        "password": password ,
                        "first_name": fake.first_name(),
                        "last_name": random.choice(noms_fon),
                        # "academy_id" : random.randint(33,37), 
                        # "level_id" : level_id,
                        # "subject_id" : subject_id,
                        "starting_year_in_academy": (datetime.today() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                        "title" : random.choice(titles),
                        # "active" : True,
                        "type_user": "teacher",
                        "phone_number": fake.phone_number(),
                    })
        
        file_path="infos_teachers.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_dict,f,indent=4,ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f"{nbr_teachers} posts d'enseingnants créés avec succès !"))