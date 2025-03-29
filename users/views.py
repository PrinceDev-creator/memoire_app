from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, serializers 
from rest_framework.permissions import IsAuthenticated,AllowAny 
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from dj_rest_auth.registration.views import RegisterView
# from users.serializers import CustomRegisterSerializer
from note.serializers import NoteSerializer
from subject.models import Subject
from .models import Teacher, Academy ,Tutor, UserApp
from note.models import Note
from students.models import Student
from users.models import Tutor
from .serializers import TeacherSerializer, AcademySerializer,TutorSerializer,UserSerializer,CustomLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.management.commands import auto_seed_academy_level_subject

# from django_otp.plugins.otp_email.models import EmailDevice


# config{
#     apiKey: "AIzaSyA5cN3922Lvu5nKXNiSsWwRL4vqg2ReI8I",
#     authDomain: "ojuapp.firebaseapp.com",
#     projectId: "ojuapp",
#     storageBucket: "ojuapp.firebasestorage.app",
#     messagingSenderId: "711396295912",
#     appId: "1:711396295912:web:16694904ddd092fdd9355d"
# }

# class CustomRegisterView(RegisterView):
#     serializer_class = CustomRegisterSerializer
#     permission_classes = [AllowAny]  # Permet l'inscription sans authentification
    
#     @method_decorator(csrf_exempt)  # Désactive CSRF pour cette vue
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
    
#     # Appliquer le décorateur ici sur la méthode
#     # def post(self, request, *args, **kwargs):
#     #     """
#     #     Personnalise la vue POST pour désactiver CSRF uniquement pour cette méthode.
#     #     """
#     #     return super().post(request, *args, **kwargs)
    
    
#     def get_response_data(self, user):
#         """
#         Personnalise la réponse après l'inscription en renvoyant les détails de l'utilisateur.
#         """
#         # return {
#         #     "id": user.id,
#         #     "username": user.username,
#         #     "email": user.email
#         #     # "type_user": user.type_user,  # Assure-toi que ce champ existe
#         # }
        
#         return user


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet pour l'inscription des utilisateurs """
    
    queryset = UserApp.objects.all()
    serializer_class = UserSerializer
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
                        "tutor": (user.tutors.first_name, user.tutors.last_name) if hasattr(user,'tutors') and user.is_tutor else None,
                        # "Teacher" : user.first_name if user.is_tacher else None
                    }
                }, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                return Response(f"Erreur d'intégrité: {str(e)}",status=status.HTTP_400_BAD_REQUEST)
            except Exception as e :
                return Response(f"Erreur : {str(e)}",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]  # L'accès est autorisé sans authentification préalable

    def post(self, request, *args, **kwargs):
        
        print(f"request data :{request.data}")
        
        serializer = CustomLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            response = serializer.validated_data
            message=response['message']['message']
            if message=='Connexion réussie':
                return Response({
                        "message" : message
                    }, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({
                   "message": message 
                  },status=status.HTTP_401_UNAUTHORIZED)
                    
        return Response(serializer.errors, status=400)
    
            # user = serializer.validated_data['user']
            # type_user = serializer.validated_data['type_user']
            
            # if type_user=="academy":
            #     academy=serializer.validated_data['academy']

            #     # Création d'un token JWT
            #     # refresh = RefreshToken.for_user(user)
            #     # access_token = refresh.access_token

            #     # Réponse personnalisée avec le token et l'académie
            #     return Response({
            #         # 'token': str(access_token),
            #         'academy': academy
            #     })
            # elif type_user=='teacher':
            #     teacher=serializer.validated_data['user']
            #     message=serializer.validated_data['message']
                
    
    
       
class TestView(APIView):
     def get(self, request):
         return Response({"message" : "CSRF désactivé"})     
        
    
# class UserRegisterView(viewsets.ModelViewSet):
#     # authentication_classes = []  # Désactive l'authentification
#     permission_classes = [IsAuthenticated,] 
    
    # @method_decorator(csrf_exempt)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     # print(request.data)
    #     # serializer = UserRegistrationSerializer(data=request.data)
    #     # if serializer.is_valid():
    #     #     user = serializer.save()
    #     #     return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
    #     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"message" : "CSRF désactivé"})

# class UserDetailView(APIView):
    
#     # permission_classes=[IsAuthenticated,]
    
#     def get(self, request, user_id, *args, **kwargs):
#         try:
#             user = UserApp.objects.get(id=user_id)
#             serializer = UserRegistrationSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except UserApp.DoesNotExist:
#             return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

#     def post(self, request, *args, **kwargs):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "Utilisateur créé avec succès", "user_id": user.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, user_id, *args, **kwargs):
#         try:
#             user = UserApp.objects.get(id=user_id)
#             serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except UserApp.DoesNotExist:
#             return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, user_id, *args, **kwargs):
#         try:
#             user = UserApp.objects.get(id=user_id)
#             user.delete()
#             return Response({"message": "Utilisateur supprimé"}, status=status.HTTP_204_NO_CONTENT)
#         except UserApp.DoesNotExist:
#             return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)


class AdminAcademyView(viewsets.ModelViewSet):
    queryset=Academy.objects.all()
    serializer_class=AcademySerializer
    permission_classes = [AllowAny]

class AcademyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Academy.objects.all()
    # permission_classes=[IsAuthenticated,]
    serializer_class=AcademySerializer
    
    
    # @staticmethod
    # def update_discipline_note(new_note, cycle, student, subject):
    #     try:
    #         if subject == 'discipline_note':
    #             note = Note.objects.get(student=student, cycle=cycle, subject=subject)
    #             note.note = new_note
    #             note.save()
    #         else:
    #             return "L'Academy  ne peut modifier que la note de conduite"
    #     except Note.DoesNotExist:
    #         print('Aucune note ne correspond aux critères fournis')
    #     except Note.ValueError as ve:
    #         print(f"Valeurs erronées des paramètres : {ve}")
    #     except Exception as e:
    #         print(f"Erreur inattendu : {e}")
    
    
    # @staticmethod
    # def insert_teacher(name, level, subject):
    #     Teacher(name=name, level=level, subject=subject)
    
    # @staticmethod
    # def update_teacher(new_name, level, subject):
    #     teacher = Teacher.objects.get(level=level, subject=subject)
    #     teacher.name = new_name
    #     teacher.save()
    
    # @staticmethod
    # def create_student(name, Academy , level, registration_number, photo, year_Academy ):
    #     Student(name=name, Academy =Academy , registration_number=registration_number, level=level, photo=photo,
    #             year_Academy =year_Academy )
    
    # @staticmethod
    # def update_student(Academy , year_Academy , registration_number, new_name, new_photo, repeating):
    #     student = Student.objects.get(Academy =Academy , year_Academy =year_Academy , registration_number=registration_number)
    #     student.name = new_name
    #     student.photo = new_photo
    #     student.repeating = repeating
    #     student.save()
    
    
    # @staticmethod
    # def enabled_account(user, user_pk):
    #     match user:
    #         case 'enseignant':
    #             Teacher.objects.get(pk=user_pk).activate = True
    #         case 'parent':
    #             Tutor.objects.get(pk=user_pk).activate = True
    
    # @staticmethod
    # def disabled_account(user, user_pk):
    #     match user:
    #         case 'enseignant':
    #             Teacher.objects.get(pk=user_pk).activate = False
    #         case 'parent':
    #             Tutor.objects.get(pk=user_pk).activate = False

class AdminTeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [IsAuthenticated,]
   

def run_auto_seed_teachers(request): 
    auto_seed_academy_level_subject.seed_teachers()
    return JsonResponse({"message" :"Les clés d'enseignants sont créées"})
    


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [IsAuthenticated,]
    

    # def __str__(self):
    #     return f"{self.name}, {self.email}, {self.starting_year_in_Academy },{self.title}"

    
    # def create_teacher(request):
    #     if request.method == "POST":
    #         teacher_id = request.POST.get("teacher_id")
    #         name = request.POST.get("name")
    #         email = request.POST.get("email")
    #         subject = request.POST.get("subject")

    #         message = add_teacher(teacher_id, name, email, subject)
    #         return JsonResponse({"message": message})

    #     return JsonResponse({"error": "Méthode non autorisée"}, status=400)



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
    


class AdminTutorViewSet(viewsets.ModelViewSet):
    queryset=Tutor.objects.all()
    serializer_class=TutorSerializer
    # permission_classes=[IsAuthenticated,]
    
    # def insert_tutor(self, student_id):
    #     student=Student.objects.get(pk=student_id)
    #     student.tutor=self
    #     student.save()


    
class TutorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Tutor.objects.all()
    serializer_class=TutorSerializer
    # permission_classes=[IsAuthenticated,]
    
    # def insert_tutor(self, student_id):
    #     student=Student.objects.get(pk=student_id)
    #     student.tutor=self
    #     student.save()
        
        
# class VerifyOTP(APIView):
#     permission_classes = [IsAuthenticated]  # Assurez-vous que l'utilisateur est authentifié

#     def post(self, request, *args, **kwargs):
#         otp_code = request.data.get('otp_code')  # Code OTP envoyé par l'utilisateur
#         if not otp_code:
#             return Response({"error": "OTP code is required"}, status=400)

#         user = request.user
#         otp_device = EmailDevice.objects.get(user=user)

#         if otp_device.verify_token(otp_code):  # Vérifie si le code est correct
#             return Response({"message": "OTP Verified Successfully"}, status=200)
#         else:
#             return Response({"error": "Invalid OTP code"}, status=400)

