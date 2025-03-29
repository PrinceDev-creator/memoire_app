import random
from faker import Faker
from users.models import Academy, UserApp
from django.core.management import BaseCommand
from django.contrib.auth.hashers import make_password
# from utils.helps import lowercase_first_letter

fake=Faker()

for i in range(5):
    last_user=Academy.objects.last()
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
        nbr_academies=int(input("Veuillez entrer le nombre d'école à créer: "))
        if nbr_academies > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")


def lowercase_first_letter(s):
    return s[0].lower() + s[1:] if s else s


class Command(BaseCommand):
    def handle(self,**kwargs):
        users=[]
        academies=[]
        
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
        
        initial_academy=['Complexe scolaire', 'CEG', 'Lycée']
        first_name=fake.first_name()
        director=f"{random.choice(noms_fon)} {first_name}"
        place=random.choice(benin_addresses)
        academy=f"{initial_academy} {fake.name()}"
        email=f"{lowercase_first_letter(first_name)}{fake.email()}"
        password='academyPassword'
        
        for i in range(nbr_academies):
            
            first_name=fake.first_name()
            director=f"{random.choice(noms_fon)} {first_name}"
            place=random.choice(benin_addresses)
            academy=f"{random.choice(initial_academy)} {fake.name()}"
            email=f"{lowercase_first_letter(first_name)}{fake.email()}"
            password='academyPassword'
            
            
            while UserApp.objects.filter(email=email).exists():
                email=f"{director}{fake.email()}"
            
            user=UserApp(
                email=email,
                password=make_password(password),
                is_academy=True,
                first_connexion=None,
            )
            
            academy=Academy(
                user=user,
                director=director,
                academy=academy,
                place=place
            )
        
            users.append(user)
            academies.append(academy)
        
        UserApp.objects.bulk_create(users)
        Academy.objects.bulk_create(academies)
        
    
        self.stdout.write(self.style.SUCCESS(f"{nbr_academies} écoles créées"))
    
    
    