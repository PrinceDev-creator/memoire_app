from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from .models import UserApp,Teacher,Tutor
from django.core.exceptions import ObjectDoesNotExist

User=UserApp

class CustomAuthBackend(BaseBackend):
    
    @staticmethod
    def authenticate(email =None, password =None, **kwargs):
        print(f" emailAuth:{email}, passwordAuth: {password}")
        # password=make_password(password)
        user=User.objects.filter(email=email).exists()
        print(user)
        try:
            if User.objects.filter(email=email).exists():
              user=User.objects.get(email=email)
              if user.check_password(password):
                return Response({"user": user.email, "message": "Connexion réussie"},status=status.HTTP_200_OK)
               
        except ObjectDoesNotExist:
            return Response({"message" : "Aucun utilisateur trouvé, veuillez vérifier les informations saisies"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Erreur est survenue {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Authentification échouée"}, status=status.HTTP_401_UNAUTHORIZED)

        # if type_user == 'academy':
            #     user=User.objects.get(email=email)
            #     if user and user.check_password(password):
            #         return Response({"user": user, "message": "Connexion école"},status=status.HTTP_200_OK)
            # if type_user =='teacher' or type_user=='tutor':
            #         if User.objects.filter(email=email, password=password).exists:
            #             user=User.objects.get(email=email,password=password)
            
            
             # else :
                #     user=User.objects.get(user_key=user_key)
                #     if user.first_connexion :
                #         user.email=email
                #         user.password=make_password(password)
                #         user.first_connexion=False
                #         user.save()
                #         return Response({"user": user, "message":"Inscription"},status=status.HTTP_201_CREATED)
                #     else:
                #         return  Response({"message":"Vous êtes déjà inscrit, entrez juste votre email et votre mot de passe"})