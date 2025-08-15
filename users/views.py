import random
import string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from requests import request
from rest_framework.response import Response
from rest_framework import viewsets, serializers 
from rest_framework.permissions import IsAuthenticated,AllowAny 
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from dj_rest_auth.registration.views import RegisterView
# from users.serializers import CustomRegisterSerializer
from note.serializers import NoteSerializer
from pre_registration.models import PreRegistration
from subject.models import Subject
from users.authentication import CustomAuthBackend 
from users.models import Teacher
from users.models import Academy
from users.models import Tutor
from note.models import Note
from students.models import Student
from users.models import Tutor
from teacher.serializers import ProfilTeacherSerializer
from tutor.serializers import ProfilTutorSerializer
from animation.models import Animation
from .serializers import GenerateTeacherKeySerializer, TeacherSerializer, AcademySerializer,UserRegisterSerializer,CustomLoginSerializer,UserViewSerializer,UserCreationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.management.commands import auto_seed_academy_level_subject
from school.serializers import SchoolSerializer
from pre_registration.serializers import PreRegistrationSerializer
from utils.helps import send_email_with_html_body

User=get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet pour l'inscription des utilisateurs """
    
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ["post"]  # On autorise seulement la création

    def create(self, request, *args, **kwargs):
        """ Surcharge de la méthode pour personnaliser la réponse """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    "message": "Utilisateur inscrit avec succès",
                    "user_data": {
                        "id": user.id,
                        # "username": user.username,
                        "email": user.email,
                        "type_user": "Academy" if user.is_academy else "Teacher" if user.is_teacher else "Tutor",
                        "academy": user.academies.academy if hasattr(user,'academies') and  user.is_academy else None,
                        "teacher": (user.teachers.first().first_name, user.teachers.first().last_name) if user.teachers.exists() and user.is_teacher else None,
                        "tutor": (user.tutors.first().first_name, user.tutors.first().last_name) if user.tutors.exists() and user.is_tutor else None,
                        # "Teacher" : user.first_name if user.is_tacher else None
                    }
                }, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response(f"Erreur d'intégrité: {e}",status=status.HTTP_400_BAD_REQUEST)
            except Exception as e :
                return Response(f"Erreur : {e}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserRegister(APIView):
    permission_classes=[AllowAny]
    http_method_names = ['post', 'patch']
    
    def post(self, request,*args, **kwargs):
        
        print(f'request_data : {request.data}')
        
        data=request.data.copy()
        type_user=data.get('type_user')
    
        if type_user=='academy':
            
            data['connexion_key']=self.generate_connexion_key()
            # preg_id_list=data.pop('preg_id')
            # preg_id=preg_id_list[0]
            
            # print(f'preg_id : {preg_id}')
            # # data['password']=None
            
            print(f"academy_data : {data}")
            
            
            # accepted=self.update_pre_registration(id=preg_id)
            
            # print(f'accepted : {accepted}')
            
            # if accepted :
            
            user_serializer=UserCreationSerializer(data=data)
            
            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status=400)
            
            user=user_serializer.save()
            user.is_academy=True
            user.save()
            data['user']=user.id
            profil_serializer=SchoolSerializer(data=data)
            
            if not profil_serializer.is_valid():
                user.delete()
                return Response(profil_serializer.errors, status=400)
            
            profil_serializer.save()
            
            email=data['email']
            
            has_send = send_email_with_html_body(receivers=[email], subject='Clé de connexion', template='emails/connexion_key_school.html', context={'connexion_key': data['connexion_key']})
            
            if has_send:
                ctx={"msg": "Mail envoyé avec succès"}
                status=200
            else:
                ctx={"msg": "L'envoi du mail a échoué"}
                status=500
    
            return Response(ctx, status=status)

        elif type_user=='teacher':
            # animation_key=data.pop('animation_key')
            
            # animation=self.verify_validation_of_animation_key(animation_key)
            
            # if animation == None :
            #     return Response({'error': 'Vérifier la clé entrée' }, status=500)
            
            data['connexion_key']=self.generate_connexion_key()
            data['password']=make_password(data['password'])

            user_serializer=UserCreationSerializer(data=data)
            
            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status=400)
            
            user=user_serializer.save()
            user.is_teacher=True
            user.save()
            data['user']=user.id
            profil_serializer=ProfilTeacherSerializer(data=data)
            
            if not profil_serializer.is_valid():
                user.delete()
                return Response(profil_serializer.errors, status=400)
            
            profil_serializer.save()
            
            email=data['email']
            
            has_send = send_email_with_html_body(receivers=[email], subject='Clé de connexion', template='emails/connexion_key_teacher.html', context={'connexion_key': data['connexion_key']})
            
            if has_send:
                ctx={"msg": "Mail envoyé avec succès"}
                status=200
            else:
                ctx={"msg": "L'envoi du mail a échoué"}
                status=500
    
            return Response(ctx, status=status)
            
        elif type_user=='tutor':
            
            data['connexion_key']=self.generate_connexion_key()
            data['password']=make_password(data['password'])

            user_serializer=UserCreationSerializer(data=data)
            
            if not user_serializer.is_valid():
                return Response(user_serializer.errors, status=400)
            
            user=user_serializer.save()
            user.is_tutor=True
            user.save()
            
            data['user']=user.id
            profil_serializer=ProfilTutorSerializer(data=data)
            
            # else:
            #     return Response({'detail' : 'Type d\'utilisateur invalide'})
            
            print(f'request_data : {data}')
        
            if not profil_serializer.is_valid():
                user.delete()
                return Response(profil_serializer.errors, status=400)
        
            profil_serializer.save()
            
            email=data['email']
                
            has_send = send_email_with_html_body(receivers=[email], subject='Clé de connexion', template='emails/connexion_key_tutor.html', context={'connexion_key': data['connexion_key']})
            
            if has_send:
                ctx={"msg": "Mail envoyé avec succès"}
                status=200
            else:
                ctx={"msg": "L'envoi du mail a échoué"}
                status=500

            return Response(ctx, status=status)

        
        # return Response({'Utilisateur créé avec succès'},status=201)
    
    
    def patch(self, request,*args, **kwargs):
        try:
            connexion_key=request.data.get('connexion_key')
            user=User.objects.get(connexion_key=connexion_key)
            serializer=UserCreationSerializer(instance=user, data=request.data, partial=True)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            
            # print(f'serializer-return : {serializer}')
            serializer.save()
            return Response({'message': 'Mot de passe défini avec succès'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=404)        
         
    def generate_connexion_key(self):
        connexion_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        while User.objects.filter(connexion_key=connexion_key).exists():
            connexion_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        print(connexion_key)
        return connexion_key
    
    def verify_validation_of_animation_key(animation_key):
        try:
            animation=Animation.objects.filter(teacher__isnull=True, animation_key=animation_key).first()
            return animation
        except Exception as e:
            raise serializers.ValidationError(f'Une erreur s\'est produite : {e}')
        
    def update_pre_registration(self,id):
        
        print(f"id_in_func : {id}")
        
        pre_registration=PreRegistration.objects.get(id=id)
        
        print(f'preg_obj : {pre_registration}')
        
        data={}
        data['accepted']=True
        
        print(f'data: {data}')
        
        serializer=PreRegistrationSerializer(instance=pre_registration, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return True
        else :
            return False   
            

class CustomLoginView(APIView):
    permission_classes = [AllowAny]  # L'accès est autorisé sans authentification préalable

    def post(self, request, *args, **kwargs):
        
        print(f"request data :{request.data}")
        
        serializer = CustomLoginSerializer(data=request.data)
        
        auth=CustomAuthBackend()
        
        if  serializer.is_valid():
            # response = serializer.validated_data
            # message=response['response']['message']
            # if message=='Connexion réussie':
            #     return Response({
            #             "user" : response['response']['user'],
            #             "message": message
            #         }, status=status.HTTP_202_ACCEPTED)
            # else:
            #     return Response({
            #        "message": message 
            #       },status=status.HTTP_401_UNAUTHORIZED)
            data=serializer.validated_data
            
            response=auth.authenticate(email=data['email'], password=data['password'], type_user=data['type_user'], connexion_key=data['connexion_key'])
            return response              
        
        return Response(serializer.errors, status=400)
    
   
class DefPassword(APIView):
    
     def patch(self, request,*args, **kwargs):
        try:
            connexion_key=request.data.get('connexion_key')
            connexion_key_user=str(connexion_key).strip()
            print(f'connexion_key : {connexion_key_user}')
            # users=User.objects.all()
            # print('users: ',users)
            user=User.objects.get(connexion_key=connexion_key_user)
            print('user :', user)
            serializer=UserCreationSerializer(instance=user, data=request.data, partial=True)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            
            # print(f'serializer-return : {serializer}')
            elif serializer.is_valid():
                serializer.save()
                
            return Response({'message': 'Mot de passe défini avec succès'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=400)
        except Exception as e:
             return Response({'error': str(e)}, status=400)
   
       
class TestView(APIView):
     def get(self, request):
         return Response({"message" : "CSRF désactivé"})     
        
        
  

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class = UserViewSerializer
    

class AdminAcademyViewSet(viewsets.ModelViewSet):
    queryset = Academy.objects.all()
    serializer_class = AcademySerializer
    # permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        queryset = Academy.objects.all()
        
        user_id=self.request.GET.get('user')
        
        if user_id is not None:
            queryset=Academy.objects.filter(user_id=user_id)
        return queryset


      
class AcademyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Academy.objects.all()
    serializer_class = AcademySerializer
    # permission_classes = [IsAuthenticated,]


class AdminTeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    # permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        
        print('enterQuerySetFunc')
        # subject_id=self.request.GET.get('subject')
        queryset=Teacher.objects.all()
        
        level_id=self.request.GET.get('level')
        user_id=self.request.GET.get('user')
        teacher_key=self.request.GET.get('key')
        
        if level_id is not None:
            print(f'levelId : {level_id}')
            queryset = Teacher.objects.filter(level_id=level_id)
        elif user_id is not None and teacher_key is not None:
            queryset = Teacher.objects.filter(user_id=user_id, teacher_key=teacher_key)
        return queryset
        
def run_auto_seed_teachers(request): 
    
    num_academy=input("Entrer le numéro de l'école: ")

    num_academy=int(num_academy)
    auto_seed_academy_level_subject.seed_teachers(academy_id=num_academy)
    return JsonResponse({"message" :"Les clés d'enseignants sont créées"})
    

class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeacherSerializer
    # permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        queryset=Teacher.objects.all()
        return queryset 

    def update_teacher(self, name, email, password, starting_year_in_Academy , title):
        self.name = name
        self.password = password
        self.email = email
        self.starting_year_in_Academy  = starting_year_in_Academy 
        self.title = title
        self.save()

    @action(detail=True ,methods=['post'], url_path='create-note')
    def create_note(self, note, quiz, cycle, student, subject):
        Note(note=note, quiz=quiz, cycle=cycle, teacher=self, student=student, subject=subject)


    def update_note(self, student, quiz, cycle, new_note, subject):
        try:
            note = Note.objects.get(student=student, teacher=self, subject=subject, cycle=cycle, quiz=quiz)
            note.note = new_note
            note.save()
        except Note.DoesNotExist:
            print('Aucune note ne correspond aux critères fournis')
        except Note.ValueError as ve:
            print(f"Valeurs erronées des paramètres : {ve}")
        except Exception as e:
            print(f"Erreur inattendu : {e}")

    
    @staticmethod
    def get_all_student_notes():
        return Note.objects.all()
    

# class AdminTutorViewSet(viewsets.ModelViewSet):
#     queryset=Tutor.objects.all()
#     serializer_class=TutorSerializer
#     # permission_classes=[IsAuthenticated,]
    
    
# class TutorViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset=Tutor.objects.all()
#     serializer_class=TutorSerializer
#     # permission_classes=[IsAuthenticated,]

class GenerateTeacherKeyView(viewsets.ModelViewSet):
    queryset=Teacher.objects.all()
    serializer_class=GenerateTeacherKeySerializer