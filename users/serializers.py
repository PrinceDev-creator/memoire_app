from django.db import IntegrityError,DatabaseError
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.contrib.auth.hashers import make_password
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
import random,string
from level.models import Level
from subject.models import Subject
from users.models import Teacher, Academy , Tutor
from level.serializers import LevelSerializer
from subject.serializers import SubjectSerializer
# from note.models import Note
# from django.contrib.auth import authenticate
from users.authentication import CustomAuthBackend
from .models import UserApp, Academy  # Assure-toi que ton modèle User et Academy sont importés


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ Serializer pour l'inscription d'un utilisateur """
    
    type_user = serializers.ChoiceField(choices=[("academy", "Academy"), ("teacher", "Teacher"), ("tutor", "Tutor")])
    teacher_key=serializers.CharField(max_length=100, required=False, allow_blank=True)
    tutor_key=serializers.CharField(max_length=100, required=False, allow_blank=True)
    first_name=serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name=serializers.CharField(max_length=100, required=False, allow_blank=True)
    academy = serializers.CharField(max_length=100, required=False, allow_blank=True)
    academy_id = serializers.IntegerField(required=False)
    level_id = serializers.IntegerField(required=False)
    subject_id = serializers.IntegerField(required=False)
    student_id = serializers.IntegerField(required=False)
    starting_year_in_academy = serializers.CharField(max_length=100, required=False, allow_blank=True)
    title = serializers.CharField(max_length=100, required=False, allow_blank=True)
    place=serializers.CharField(max_length=128, required=False, allow_blank=True)
    director=serializers.CharField(max_length=100, required=False, allow_blank=True)
    

    class Meta:
        model = User
        fields = ["id", "password", "email", "type_user","teacher_key","tutor_key", "academy", "academy_id","student_id", "level_id", "subject_id", "starting_year_in_academy","title","first_name", "last_name","place","director"]
        extra_kwargs = {"password": {"write_only": True}}  # Ne pas afficher le password dans la réponse

    def create(self, validated_data):
        try:
            fields_as_type_user=["academy", "type_user","academy_id","student_id", "level_id", "teacher_key","tutor_key","subject_id", "starting_year_in_academy","title","place","director"]
            dict_field_as_type_user=dict()
            
            """Parcours la liste de champ associé à un certain type d'utilisateur et extraire les valeurs correspondantes"""
            dict_field_as_type_user=UserSerializer.sort_validated_data(fields=fields_as_type_user,validated_data=validated_data)
            
            print(f"validated_data : {validated_data}, dict_field_as_type_user : {dict_field_as_type_user}")
            
            """Vérifie si la clé d'utilisateur est présente, si oui l'affecte à une variable"""
            if dict_field_as_type_user.get('teacher_key') !=None:
                verify_teacher=UserSerializer.verify_uniqueness_of_teacher_key(teacher_key=dict_field_as_type_user['teacher_key'])
                if isinstance(verify_teacher,Teacher):
                    print(f" verify_teacher : {verify_teacher}")
                else :
                    print("Erreur")    
            
            """Hash le mot de passe et l'affecte à une variable ainsi que l'email"""
            validated_data["password"] = make_password(validated_data["password"])
            password=validated_data['password']
            email=validated_data.get('email')
            
            if email==None :
                raise ValueError("Informations incorrectes")

            type_user=dict_field_as_type_user['type_user']
            
            # Attribution du rôle
            if type_user == "academy":
                if UserSerializer.verify_academy_in_user_table(email=email):
                    raise IntegrityError("Un utilisateur utilisant ce email existe déjà")
                user = User.objects.create(**validated_data)
                user.is_academy = True
                user.save()
                academy=dict_field_as_type_user['academy']
                director=dict_field_as_type_user['director']
                place=dict_field_as_type_user['place']
                UserSerializer.sign_up_academy(user=user, academy=academy, director=director, place=place)
                
                    
            elif type_user == "teacher" and isinstance(verify_teacher,Teacher):
                
                print(f'type_user: {type_user}')
                
                teacher_key=dict_field_as_type_user['teacher_key']
                starting_year_in_academy=dict_field_as_type_user['starting_year_in_academy']
                title=dict_field_as_type_user['title']
                first_name=validated_data.get('first_name') 
                last_name=validated_data.get('last_name')
                
                user=UserSerializer.get_or_create_user(email, password ,first_name ,last_name, type_user)  
                user.save()
                print(f"user: {user}")
               
                response=UserSerializer.sign_up_teacher(user=user, teacher_key=teacher_key, starting_year_in_academy=starting_year_in_academy,first_name=first_name, last_name=last_name,title=title)
                print(response)
                
            elif type_user == "tutor":
                user.is_tutor = True
                user.save()
                first_name=dict_field_as_type_user['first_name']
                last_name=dict_field_as_type_user['last_name']     
                Tutor.objects.create(user=user,first_name=first_name ,last_name=last_name)
            
            return user
        
        except IntegrityError as e:
            raise serializers.ValidationError(f" Erreur d'intégration dans la base de donnée : {e}")
        except Exception as e:
            raise serializers.ValidationError(f"Une erreur est survenue: {e}")
        
    @staticmethod
    def detect_duplicate_academy_level_subject(academy_id,level_id,subject_id): 
        if Teacher.objects.filter(academy_id=academy_id, level_id=level_id, subject_id=subject_id).exists():
            return 
        else :
            return [(academy_id, level_id, subject_id)]
        
    @staticmethod    
    def detect_duplicate_user_key(user_key):
        while User.objects.filter(user_key=user_key).exists():
                user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        print(user_key)
        return user_key
        
    @staticmethod    
    def detect_duplicate_email(email):
        if User.objects.filter(email=email).exists():
            return None
        else :
            return email
    @staticmethod
    def sign_up_teacher(teacher_key,title,starting_year_in_academy,first_name, last_name, user):
        try:
            teacher=Teacher.objects.get(teacher_key=teacher_key) 
            teacher.user=user
            teacher.first_name=first_name
            teacher.last_name=last_name
            teacher.starting_year_in_academy=starting_year_in_academy
            teacher.title=title
            teacher.save()
            return True
        except Exception as e : 
            raise serializers.ValidationError(f'Erreur : {str(e)}')
    
    @staticmethod
    def sign_up_academy(director,place,academy,user):
        try:
            academy_obj=Academy.objects.create(user=user, academy=academy , place=place ,director=director) 
            return academy_obj
        except Exception as e : 
            raise serializers.ValidationError(f'Erreur : {str(e)}')
        
    @staticmethod    
    def verify_uniqueness_of_teacher_key(teacher_key):
        try:
            teacher=Teacher.objects.filter(
                Q(user__isnull=True)
            ).get(teacher_key=teacher_key)
            return teacher    
        
        except Teacher.DoesNotExist:
            return f"Une erreur s'est produite"
        except MultipleObjectsReturned:
            return "Erreur : Plusieurs enseignants correspondent à cette clé."
        except IntegrityError as e:
            return f"Erreur d'intégrite : {e}"
        except Exception as e:
            return f"Erreur : {e}"
            
    @staticmethod    
    def verify_tutor(tutor_key):
        tutor_exists=Tutor.objects.filter(tutor_key=tutor_key).exists()
        return tutor_exists
    
    @staticmethod        
    def verify_teacher_in_user_table(email):
        teacher_exists=User.objects.filter(email=email, is_teacher=True).exists()
        return teacher_exists
    
    @staticmethod
    def verify_academy_in_user_table(email):
        academy_exists=User.objects.filter(email=email, is_academy=True).exists()
        return academy_exists
    
    @staticmethod
    def sort_validated_data(fields,validated_data):
        dict_field_as_type_user = {}
        for field in fields:
            if field in validated_data:  # Vérifier si le champ existe
                dict_field_as_type_user[field] = validated_data.pop(field)  # Extraire la valeur

        return dict_field_as_type_user
       
    @staticmethod    
    def search_user(email):
        user=User.objects.filter(email).first()
        return user
    
    @staticmethod
    def get_or_create_user(email, password,first_name, last_name, type_user):
        
        is_teacher_or_tutor=""
        is_teacher_or_tutor="is_teacher" if type_user=="teacher" else "is_tutor"
        print(f'is_tea_tu: {is_teacher_or_tutor}')

        user,created=User.objects.get_or_create(
            email=email,
            defaults={"password": password,"first_name": first_name, "last_name": last_name, is_teacher_or_tutor :True}
        )
        if created:
            print(f"Nouvel utilisateur créé : {user}")
        else:
            print(f"Utilisateur récupéré : {user}")
        
        return user
    
  
class UserViewAfterLogin(serializers.Serializer):
    class Meta:
        model=User
        fields=['email'] 
  
class CustomLoginSerializer(serializers.Serializer):
    
    
    # username=serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # token = serializers.CharField(read_only=True)
    # academy = serializers.CharField(read_only=True)

    def validate(self, attrs):
        
        auth=CustomAuthBackend()
        email = attrs.get('email')
        password = attrs.get('password')
        
        print(f"email : {email}, password : {password}")

        try:
        # Authentification de l'utilisateur
            response = auth.authenticate(email=email, password=password) 
            print(f"response : {response.data}")
            attrs['message']=response.data
            return attrs
        except Exception as e:
            return f"error :{e}"
        
        # message=response.data['message']
        
        # if response.data['user']:
        #     user=response.data['user']
        #     if user.is_academy:
        #         try:
        #             academy_object = Academy.objects.get(user=user)
        #         except Academy.DoesNotExist:
        #             academy_object = None
        #         attrs['user'] = user
        #         attrs['type_user']="academy"
        #         attrs['academy'] = AcademySerializer(academy_object).data if academy_object else None
        #         attrs['message']= message

            
        #     elif user.is_teacher or user.is_tutor:
        #             # teacher = Teacher.objects.get(user=user)
        #             if message=="Inscription" :
        #                 attrs["message"]="Inscription de l'enseignant effectuée avec succès" if user.is_teacher else "Inscription du parent/tuteur effectuée avec succès" 
        #                 attrs['user'] = user
        #                 attrs['type_user']="teacher" if user.is_teacher else "tutor"
        #                 # attrs['teacher'] = TeacherSerializer(teacher).data if teacher else None
        #             elif message=="Connexion":
        #                 attrs["message"]="Connexion  de l'enseignant effectuée avec succès"  if user.is_teacher else "Connexion du parent/tuteur effectuée avec succès"
        #                 attrs['user'] = user
        #                 attrs['type_user']="teacher" if user.is_teacher else "tutor"
        
            # return attrs
        # else:
        #     raise AuthenticationFailed('Invalid credentials')
        

class TeacherSerializer(serializers.ModelSerializer):
    
    username=serializers.CharField(source='User.username',read_only=True)
    subject=serializers.CharField(source='subject.name', read_only=True)
    level=serializers.CharField(source='level.name', read_only=True)
    academy=serializers.CharField(source='academy.email', read_only=True)
    
    class Meta:
        model = Teacher
        fields=['id', 'username','subject','level', 'academy']  
    

class AcademySerializer(serializers.ModelSerializer):
    class Meta:
        model=Academy 
        fields=['id','academy', 'email']
        
class AcademyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Academy 
        fields=['academy','email']


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tutor
        exclude=['activate', 'id', 'password']
    
    
    
    #commentaires
    
    # academy=dict_field_as_type_user['academy_id']
                # level=dict_field_as_type_user['level_id'], 
                # subject=dict_field_as_type_user['subject_id'],
                
                # selected_value=UserSerializer.detect_duplicate_academy_level_subject(academy_id=academy,level_id=level,subject_id=subject) 
                # print(f"academy : {dict_field_as_type_user['academy_id']}, level :{dict_field_as_type_user['level_id']}, subject: {dict_field_as_type_user['subject_id']} , selected_value: {selected_value}")
                # if selected_value==None:
                #     raise IntegrityError("Cette combinaison de école/matière/classe existe déjà")
                # for academy,level,subject in selected_value: 
        
    # class UserRegistrationSerializer(serializers.ModelSerializer):
    
#     type_user=serializers.CharField()
#     academy=serializers.CharField()
    
    
#     class Meta:
#         model=User
#         fields=['username', 'email', 'password']

        
#     def create(self, validated_data):
        
#         fields_to_exclude=['type_user', 'academy', 'student', 'level', 'subject', 'starting_year_in_academy','title']
#         field_to_model=dict()
        
#         for field,value in validated_data.items():
#             if field in fields_to_exclude:
#                 field_to_model[field]=value
#                 validated_data.pop(field)
        
#         type_user=field_to_model['type_user']
#         user=User.objects.create_user(**validated_data)
        
#         if type_user=="academy":
#             user.is_academy=True
#             user.save()
#             Academy.objects.create(user=user, academy=field_to_model['academy'])
        
#         elif type_user=='tutor':
#             user.is_tutor=True
#             user.save()
#             Tutor.objects.create(user=user)
        
#         elif type_user=='teacher':
#             user.is_teacher=True
#             user.save()
#             Teacher.objects.create(user=user, academy=field_to_model['academy'], level=field_to_model['level'], subject=field_to_model['subject'], starting_year_in_academy=field_to_model['starting_year_in_academy'], title=field_to_model['title'])
        
#         return user
 
            

# class GenereateTeacherUserKey(serializers.ModelSerializer):
    
#     class Meta :
#         model = Teacher
#         fields=['user_key']
    
        
    # def create(self, validated_data):
    #     objects=
        
        
    # def update(self, instance, validated_data):
    #     teacher_key=GenereateTeacherUserKey.generate_teacher_key()
    #     instance.teacher_key=GenereateTeacherUserKey.detect_duplicate_teacher_key(teacher_key)
    #     instance.save()
    #     return instance
       
    # @staticmethod
    # def generate_teacher_key():
    #     teacher_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))        
    #     return teacher_key    
    # @staticmethod    
    # def detect_duplicate_teacher_key(teacher_key):
    #     while Teacher.objects.filter(teacher_key=teacher_key).exists():
    #             teacher_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
    #     return teacher_key
    
    
    
    
     # if attrs.get('user_key') and attrs.get('type_user'):
        #     user_key=attrs.get('user_key')
        #     type_user=attrs.get('type_user')
        #     if type_user=='teacher':
        #         if Teacher.objects.filter(user_key=user_key).first():
        #             teacher=Teacher.objects.get(user_key=user_key)
        #             teacher.first_connexion=False
        #             teacher.save()
        #     elif type_user=='tutor':
        #         if Tutor.objects.filter(user_key=user_key).first():
        #             tutor=Tutor.objects.get(user_key=user_key)
        #             tutor.first_connexion=False
        #             tutor.save()
        # else :
            
        # username=attrs.get('username')
        

    # class CustomRegisterSerializer(RegisterSerializer):
#     # type_user = serializers.CharField()

#     # def custom_signup(self, request, user):
#     #     type_user=self.validated_data.get('type_user')
#     #     # print(type_user)
#     #     if type_user=='academy':
#     #         user.is_academy=True
#     #         user.save()
#     #     elif type_user=='teacher':
#     #         user.is_teacher=True
#     #         user.save()
#     #     elif type_user=='tutor':
#     #         user.is_tutor=True
#     #         user.save()
            
#     #     email_address, created = EmailAddress.objects.get_or_create(
#     #         user=user, email=user.email, defaults={"verified": True, "primary": True}
#     #     )

#     #     # 🔹 Si l'objet existe déjà mais n'est pas vérifié, on le met à jour
#     #     if not created and not email_address.verified:
#     #         email_address.verified = True
#     #         email_address.save()    
            
#     #     # email_address = EmailAddress.objects.filter(user=user).first()
#     #     # if email_address:
#     #     #     email_address.verified = True
#     #     #     email_address.save()

        
#     #     return user
    

# class CustomRegisterSerializer(RegisterSerializer):
#     """ Personnalisation de l'enregistrement des utilisateurs """

#     type_user = serializers.ChoiceField(choices=[("academy", "Academy"), ("teacher", "Teacher"), ("tutor", "Tutor")])
#     academy = serializers.CharField(max_length=100, default=None)

#     def get_cleaned_data(self):
#         """ Permet de récupérer les données propres de l'utilisateur après validation """
#         data = super().get_cleaned_data()
#         data["type_user"] = self.validated_data.get("type_user", ""),
#         data["academy"]=self.validated_data.get("academy","")
     
#         return data

#     def save(self, request):
#         """ Sauvegarde personnalisée de l'utilisateur """
#         print('yes')
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
        
#         # 🔹 Ajout des champs personnalisés
#         type_user = self.cleaned_data.get("type_user")
#         academy = self.cleaned_data.get("academy")
#         email=self.cleaned_data.get("email")
#         print(f"academy value: {academy}") 
#         print('debut')
#         if type_user == "academy":
#             user.is_academy = True
#         elif type_user == "teacher":
#             user.is_teacher = True
#         elif type_user == "tutor":
#             user.is_tutor = True

#         user.save()

#         # 🔹 Vérifier et marquer l'email comme vérifié automatiquement
#         email_address, created = EmailAddress.objects.get_or_create(
#             user=user, email=user.email, defaults={"verified": True, "primary": True}
#         )
#         if not created and not email_address.verified:
#             email_address.verified = True
#             email_address.save()
        
        
#         # Envoi du code OTP par email
#         # otp_device = EmailDevice.objects.create(user=user, name="default")
#         # otp_device.generate_challenge()  # Génère un code OTP
#         # otp_device.save()
        
#         # if type_user == "academy":
#         #     Academy.objects.create(user=user, academy=self.cleaned_data.get("academy"))
#         # elif type_user == "teacher":
#         #     Teacher.objects.create(user=user, academy=self.cleaned_data.get("academy"))
#         # elif type_user == "tutor":
#         #     Tutor.objects.create(user=user)

#         return user