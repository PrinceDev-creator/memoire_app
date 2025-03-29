import json
import os
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
# from utils.helps import lowercase_first_letter

fake=Faker()

# print("-----Début de suppression des tuteurs----")

for i in range(5):
    last_user=Teacher.objects.last()
    if last_user:
        last_user.delete()
        print(f"Suppression {i}")
    else :
        print("Aucun tuteur trouvé")

print("-----Début de suppression des utilisateurs----")

for i in range(5):
    last_user=UserApp.objects.last()
    if last_user:
        last_user.delete()
        print(f"Suppression {i}")
    else :
        print("Aucun utilisateur trouvé")

print("-----Fin des suppressions-----")

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
        users=[]
        teachers=[]
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
            
                email=f"{fake.email()}_{random.randint(1000,9999)}"
                user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
                
                while UserApp.objects.filter(email=email).exists() and UserApp.objects.filter(user_key=user_key).exists():
                    email=f"{fake.email()}_{random.randint(1000,9999)}"
                    user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    
                
                user=UserApp(
                    # username=username,
                    # email=fake.email(),
                    is_teacher=True,
                    user_key=user_key,
                    first_connexion=True
                )
                
                # password='teacherPassword'
                
                # user.set_password(password)
                
                users_dict.append({
                        "id": user.id,
                        # "username": user.username,
                        "email" : user.email,    
                    })
                
                teacher=Teacher(
                    user=user,
                    first_name=fake.first_name(),
                    last_name=random.choice(noms_fon),
                    academy_id=random.randint(33,37),
                    level_id=level_id,
                    subject_id=subject_id,
                    starting_year_in_academy=(datetime.today() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
                    title=random.choice(titles),
                    active=True,
                    
                )
                
                users.append(user)
                teachers.append(teacher)
                    
            
        UserApp.objects.bulk_create(users)    
        Teacher.objects.bulk_create(teachers)
        
        file_path="infos_teachers.json"
        # if os.path.exists(file_path):
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         try:
        #             users_dict=json.load(f)
        #         except json.JSONDecodeError:
        #             users_dict=[]
        # else :
        #     users_dict
        
        # users_dict.append(user)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(users_dict,f,indent=4,ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f'{len(teachers)} enseingnants créés avec succès !'))