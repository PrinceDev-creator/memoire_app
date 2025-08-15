from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from school.models import School
from teacher.models import Teacher
from tutor.models import Tutor
from level.models import Level
from level.serializers import LevelSerializer
from students.models import Student
from students.serializers import StudentSerializer
from animation.models import Animation
from follow.models import Follow
from follow.serializers import FollowSerializer
from animation.serializers import AnimationSerializer
from django.core.exceptions import ObjectDoesNotExist

User=get_user_model()
academic_year=settings.ACADEMIC_YEAR

class CustomAuthBackend(BaseBackend):
    
    def authenticate(self,email=None, password =None, type_user=None ,connexion_key=None,**kwargs):
        try:
            user = self.verify_user_as_type_user(email=email, password=password, type_user=type_user, connexion_key=connexion_key)
            if user is None or not user.check_password(password):
                print(f'user : {user}')
                return Response({"message": "Authentification échouée"}, status=status.HTTP_400_BAD_REQUEST)

            # Définir data et status par défaut
            data = None
            status_code = status.HTTP_200_OK

            if user.is_academy:
                school = School.objects.get(user=user)
                levels = Level.objects.filter(school=school)
                serializer = LevelSerializer(levels, many=True)
                if serializer.data==[]:
                    data=[{'school' : school.id}]
                    return Response(data, status=status_code)
            elif user.is_teacher:
                teacher = Teacher.objects.get(user=user)
                animations = Animation.objects.filter(teacher=teacher)
                serializer=AnimationSerializer(animations, many=True)
                if serializer.data==[]:
                    data=[{'teacher_key' : teacher.user.connexion_key}]
                    return Response(data, status=status_code)
            elif user.is_tutor:
                tutor = Tutor.objects.get(user=user)
                follow_students = Follow.objects.filter(tutor=tutor, academic_year=academic_year)
                #print(f'follow_students : {follow_students}')
                serializer =FollowSerializer(follow_students, many=True)
                if serializer.data==[]:
                    data=[{'tutor_key' : tutor.user.connexion_key}]
                    return Response(data, status=status_code)

            return Response(serializer.data, status=status_code)

        except ObjectDoesNotExist:
            return Response({"message": "Utilisateur non trouvé"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Erreur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       
    def verify_user_as_type_user(self,email=None, password=None,type_user=None, connexion_key=None):
        email=email.strip()
        connexion_key=connexion_key.strip()
        if type_user=='school':  
            try:  
                user=User.objects.filter(email=email,is_academy=True, connexion_key=connexion_key).first()
                return user
            except Exception as e:
                raise Exception(f"Une erreur s'est produite {e}")
        elif type_user=='teacher':
            try:  
                user=User.objects.filter(email=email,connexion_key=connexion_key,is_teacher=True).first()
                return user
            except Exception as e:
                raise Exception(f"Une erreur s'est produite {e}")
        elif type_user=='tutor':
            try:  
                user=User.objects.filter(email=email,connexion_key=connexion_key,is_tutor=True).first()
                return user
            except Exception as e:
                raise Exception(f"Une erreur s'est produite {e}") 
       