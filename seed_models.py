# import requests

# # URL de ton API (remplace par l'URL correcte de ton serveur)
# API_URL = "http://127.0.0.1:8000/adminubjects/"  

# # Données à envoyer
# data = {
#     "subjects": [
#         {"name": "Éthique et Discipline", "category": "DISCIPLINE"},
#         {"name": "Éducation Civique", "category": "DISCIPLINE"},
#         {"name": "Sport", "category": "AUTRE"}
#     ]
# }

# # En-têtes (remplace "TonTokenIci" par ton token d'authentification si nécessaire)
# headers = {
#     "Content-Type": "application/json"
# }

# # Envoi de la requête POST
# response = requests.post(API_URL, json=data, headers=headers)

# # Affichage de la réponse
# print("Statut:", response.status_code)
# print("Réponse:", response.json())


import requests
import random
from datetime import datetime, timedelta

# URL de ton API (remplace par l'URL correcte de ton serveur)
API_URL = "http://127.0.0.1:8000/user/register/"  

# Générer des enseignants avec des valeurs aléatoires
teachers = []
for i in range(15):  # Générer 15 enseignants (modifiable)
    teacher = {
        "academy": 20,  # ID de l'école
        "level": random.randint(1, 41),  # ID du niveau entre 1 et 41
        "subject": random.randint(1, 11),  # ID de la matière entre 1 et 11
        "starting_year_in_academy": (datetime.today() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d'),
        "title": f"Professeur {i+1}",
        "active": True,
        "is_teacher": True
    }
    teachers.append(teacher)

# En-têtes (remplace "TonTokenIci" par ton token d'authentification si nécessaire)
headers = {
    "Content-Type": "application/json",
}

# Envoi de la requête POST pour chaque teacher
for teacher in teachers:
    response = requests.post(API_URL, json=teacher, headers=headers)
    print(f"Statut: {response.status_code} - Réponse: {response.json()}")
    # if response.status_code != 200:
    #     print(f"Erreur {response.status_code}: {response.text}")

