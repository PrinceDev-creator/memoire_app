import json
import string
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from level.models import Level
from subject.models import Subject
from users.models import Teacher, UserApp
from faker import Faker
import random
from datetime import datetime,timedelta
from users.utils import lowercase_first_letter

fake=Faker()


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
        selected_pair=[]

        all_pair_of_level_subject=[(level, subject) for level in range(1,42) for subject in range(1,12)]
        random.shuffle(all_pair_of_level_subject)

        for level_id,subject_id in all_pair_of_level_subject:
            try:
                if (Level.objects.get(id=level_id).DoesNotExist and Subject.objects.get(id=subject_id).DoesNotExist):
                    selected_pair+=[(level_id,subject_id)]
            except IntegrityError: 
                print("Cette combinaison de classe/matière existe déjà")
                
            if len(selected_pair)==nbr_teachers : break        
        
        print(selected_pair)    
            
        for level_id, subject_id in selected_pair:
            
            if (Level.objects.get(id=level_id).DoesNotExist and Subject.objects.get(id=subject_id).DoesNotExist):
            
                email=f"{lowercase_first_letter(fake.first_name())}{fake.email()}"
                user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
                
                while UserApp.objects.filter(email=email).exists() and UserApp.objects.filter(user_key=user_key).exists():
                    email=f"{lowercase_first_letter(fake.first_name())}{fake.email()}"
                    user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    
                
                password='teacherPassword'
                
                
                users_dict.append({
                        # "username": user.username,
                        "email" : email,
                        "password": password ,
                        "first_name": fake.first_name(),
                        "last_name": random.choice(noms_fon),
                        # "academy_id" : random.randint(33,37), 
                        # "level_id" : level_id,
                        # "subject_id" : subject_id,
                        "starting_year_in_academy": (datetime.today() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                        "title" : random.choice(titles),
                        # "active" : True,
                        "type_user": "teacher"
                    })
        
        file_path="infos_teachers.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_dict,f,indent=4,ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f"{nbr_teachers} posts d'enseingnants créés avec succès !"))