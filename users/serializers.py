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
from students.models import Student
from subject.models import Subject
from users.models import Teacher 
from users.models import Academy
from users.models import Tutor
from level.serializers import LevelSerializer
from subject.serializers import SubjectSerializer
# from note.models import Note
# from django.contrib.auth import authenticate
from pre_registration.models import PreRegistration

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    """ Serializer pour l'inscription d'un utilisateur """
    
    type_user = serializers.ChoiceField(choices=[("academy", "Academy"), ("teacher", "Teacher"), ("tutor", "Tutor")])
    level_key=serializers.CharField(max_length=100, required=False, allow_blank=True)
    student_key=serializers.CharField(max_length=100, required=False, allow_blank=True)
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
    list_student_key=serializers.JSONField(required=False)
    list_level_key=serializers.JSONField(required=False)
    

    class Meta:
        model = User
        fields = ["id", "password", "email", "type_user","level_key","student_key", "academy", "academy_id","student_id", "level_id", "subject_id", "starting_year_in_academy","title","first_name", "last_name","place","director","list_student_key","list_level_key"]
        extra_kwargs = {"password": {"write_only": True}}  # Ne pas afficher le password dans la réponse

    def create(self, validated_data):
        try:
            fields_as_type_user=["academy", "type_user","academy_id","student_id", "level_id", "level_key","student_key","subject_id", "starting_year_in_academy","title","place","director", "list_student_key","list_level_key"]
            dict_field_as_type_user=dict()
            
            """Parcours la liste de champ associé à un certain type d'utilisateur et extraire les valeurs correspondantes"""
            dict_field_as_type_user=self.sort_validated_data(fields=fields_as_type_user,validated_data=validated_data)
            
            print(f"validated_data : {validated_data}, dict_field_as_type_user : {dict_field_as_type_user}")
            
            """Vérifie si la clé d'utilisateur est présente, si oui l'affecte à une variable"""
            if dict_field_as_type_user.get('list_level_key') !=None:
                verify_teacher=self.verify_uniqueness_of_level_key(levels_keys=dict_field_as_type_user['list_level_key'])
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
                if self.verify_academy_in_user_table(email=email):
                    raise IntegrityError("Un utilisateur utilisant ce email existe déjà")
                user = User.objects.create(**validated_data)
                user.is_academy = True
                user.save()
                academy=dict_field_as_type_user['academy']
                director=dict_field_as_type_user['director']
                place=dict_field_as_type_user['place']
                self.sign_up_academy(user=user, academy=academy, director=director, place=place)
                
                    
            elif type_user == "teacher" and isinstance(verify_teacher,Teacher):
                
                print(f'type_user: {type_user}')
                
                list_level_key=dict_field_as_type_user['list_level_key']
                starting_year_in_academy=dict_field_as_type_user['starting_year_in_academy']
                title=dict_field_as_type_user['title']
                first_name=validated_data.get('first_name') 
                last_name=validated_data.get('last_name')
                validated_data['keys']=list_level_key
                # is_exist=self.verify_key_teacher(key=level_key)
                
                # if is_exist==True: 
                
                connexion_key=self.generate_connexion_key()    
                user=self.get_or_create_user(email=email, password=password ,first_name=first_name ,last_name=last_name, keys=list_level_key, connexion_key=connexion_key,type_user=type_user)  
                user.save()
                print(f"user: {user}")
                
                response=self.sign_up_teacher(user=user, list_level_key=list_level_key, starting_year_in_academy=starting_year_in_academy,first_name=first_name, last_name=last_name,title=title)
                print(response)
                # else :
                    # raise serializers.ValidationError("La clé n'existe pas")
                    
            elif type_user == "tutor":
                print(f'type_user: {type_user}')
                first_name=validated_data.get('first_name')
                last_name=validated_data.get('last_name')
                list_student_key=dict_field_as_type_user.get('list_student_key')  
                # print(f"is_exists_duplicate: { self.detect_duplicate_tutor(student_key=student_key)}, is_exists_verify : {self.verify_student_key_exists(student_key=student_key)}")
                is_exist=self.verify_keys_on_tutor(keys=list_student_key)
                print(f"is_exist : {is_exist}")
                try:
                    # if self.verify_student_key_exists(student_key=student_key) and not self.detect_duplicate_tutor(student_key=student_key):
                    if is_exist==True:   
                        print('ok')
                        user=self.get_or_create_user(email=email,password=password, first_name=first_name, last_name=last_name, keys=list_student_key)
                        user.save()
                        print('user_save')
                        connexion_key=self.generate_connexion_key()
                        print(f"connexion_key : {connexion_key}")
                        Tutor.objects.create(user=user,first_name=first_name,last_name=last_name,list_student_key=list_student_key,connexion_key=connexion_key)
                    else :
                       raise serializers.ValidationError(f"Une erreur s'est produite : les clés d'étudiants ne sont pas valides")     
                except Exception as e:
                    raise serializers.ValidationError(f"Une erreur s'est produite {e}")
                
            return user
        
        except IntegrityError as e:
            raise serializers.ValidationError(f" Erreur d'intégration dans la base de donnée : {e}")
        except Exception as e:
            raise serializers.ValidationError(f"Une erreur est survenue: {e}")
        
    
    # def verify_key_teacher(self,key):
    #     is_exist=False
    #     is_exist=Teacher.objects.filter(level_key=key, user_id__isnull=True).exists()
    #     return is_exist
     
    def verify_keys_on_tutor(self,keys):
        is_exist=True
        for key in keys:
            key_exist=Student.objects.filter(student_key=key).exists() 
            if not key_exist :
                is_exist=False
                return is_exist
        return is_exist       
        
    def generate_connexion_key(self):
        connexion_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        while Tutor.objects.filter(connexion_key=connexion_key).exists():
            connexion_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        print(connexion_key)
        return connexion_key
    
        
    def detect_duplicate_academy_level_subject(self,academy_id,level_id,subject_id): 
        if Teacher.objects.filter(academy_id=academy_id, level_id=level_id, subject_id=subject_id).exists():
            return 
        else :
            return [(academy_id, level_id, subject_id)]
         
    def detect_duplicate_user_key(self,user_key):
        while User.objects.filter(user_key=user_key).exists():
                user_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        print(user_key)
        return user_key
    
    def detect_duplicate_email(self,email):
        if User.objects.filter(email=email).exists():
            return None
        else :
            return email
        
    def sign_up_teacher(self,list_level_key,title,starting_year_in_academy,first_name, last_name, user):
        try:
            for level_key in list_level_key:    
                teacher=Teacher.objects.filter(level_key=level_key).first() 
                teacher.user=user
                teacher.first_name=first_name
                teacher.last_name=last_name
                teacher.starting_year_in_academy=starting_year_in_academy
                teacher.title=title
                teacher.save()
            return True
        except Exception as e : 
            raise serializers.ValidationError(f'Erreur : {str(e)}')
    
    def sign_up_academy(self,director,place,academy,user):
        try:
            academy_obj=Academy.objects.create(user=user, academy=academy , place=place ,director=director) 
            return academy_obj
        except Exception as e : 
            raise serializers.ValidationError(f'Erreur : {str(e)}')
          
    def verify_uniqueness_of_level_key(self,levels_keys):
        try:
            for level_key in levels_keys:
                teacher=Teacher.objects.filter(
                Q(user__isnull=True)
              ).get(level_key=level_key)
            return teacher    
        
        except Teacher.DoesNotExist:
            return f"Une erreur s'est produite"
        except MultipleObjectsReturned:
            return "Erreur : Plusieurs enseignants correspondent à cette clé."
        except IntegrityError as e:
            return f"Erreur d'intégrite : {e}"
        except Exception as e:
            return f"Erreur : {e}"
            
    def verify_tutor(self,tutor_key):
        tutor_exists=Tutor.objects.filter(tutor_key=tutor_key).exists()
        return tutor_exists
            
    def verify_teacher_in_user_table(self,email):
        teacher_exists=User.objects.filter(email=email, is_teacher=True).exists()
        return teacher_exists
    
    def verify_academy_in_user_table(self,email):
        academy_exists=User.objects.filter(email=email, is_academy=True).exists()
        return academy_exists
    
    def sort_validated_data(self,fields,validated_data):
        dict_field_as_type_user = {}
        for field in fields:
            if field in validated_data:  # Vérifier si le champ existe
                dict_field_as_type_user[field] = validated_data.pop(field)  # Extraire la valeur

        return dict_field_as_type_user
       
    def search_user(self,email):
        user=User.objects.filter(email).first()
        return user
    
    def get_or_create_user(self,email, password,first_name, last_name, keys,connexion_key,type_user):
        
        is_teacher_or_tutor=""
        is_teacher_or_tutor="is_teacher" if type_user=="teacher" else "is_tutor"
        print(f'is_tea_tu: {is_teacher_or_tutor}')
        
        user,created=User.objects.get_or_create(
            email=email,
            defaults={"password": password,"first_name": first_name, "last_name": last_name, "keys": keys, "connexion_key" : connexion_key, is_teacher_or_tutor :True}
        )
        
        if created:
            print(f"Nouvel utilisateur créé : {user}")
        else:
            print(f"Utilisateur récupéré : {user}")
        
        is_exist=User.objects.filter(keys)    
        
        return user
    
    def detect_duplicate_email_as_type_user(self,email, type_user):
        is_exist=False
        if type_user=='academy':
           is_exist=User.objects.filter(email=email, is_academy=True).exists()
        elif type_user=='teacher':
           is_exist=User.objects.filter(email=email, is_teacher=True).exists()
        elif type_user=='tutor':
           is_exist=User.objects.filter(email=email, is_tutor=True).exists()
        return is_exist
        
    def verify_student_key_exists(self,student_key):
        is_exists=False
        is_exists=Student.objects.filter(student_key=student_key).exists()
        return is_exists
    
    def detect_duplicate_tutor(self,student_key):
        is_exists=False
        is_exists=Tutor.objects.filter(student=student_key).exists()
        return is_exists
    
  
class UserViewAfterLogin(serializers.Serializer):
    class Meta:
        model=User
        fields=['email'] 
  
  
class UserCreationSerializer(serializers.ModelSerializer):
    
    preg_id=serializers.IntegerField(required=False, allow_null=True)
    # accepted=serializers.BooleanField(required=False, allow_null=True)
    
    class Meta:
        model=User
        fields=['email', 'password', 'connexion_key','preg_id'] 
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, attrs):
        # if attrs.get('email'):
        #     raise serializers.ValidationError("L'email est requis")
        # if attrs.get('connexion_key'):
        #     raise serializers.ValidationError("La clé de connexion est requise")
        if attrs.get('password') and len(attrs.get('password'))  < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères")    
        
        return attrs

    def create(self, validated_data):
        print(f'validated_data : {validated_data}')
        
        preg_id=None
        
        if validated_data.get('preg_id')!=None:
            preg_id=validated_data.pop('preg_id')
        # accepted=validated_data.pop('accepted')
        
        if preg_id!=None:
           pre_reg=PreRegistration.objects.filter(id=preg_id).first()
           if pre_reg==None:
               raise serializers.ValidationError("L'école n'existe pas")
           pre_reg.state=True 
           pre_reg.save() 
          
        
        user=User.objects.create(**validated_data)
        
        return user
    
    def update(self, instance, validated_data):
        print(f"validated_data_upd : {validated_data}")
        
        password = validated_data.get('password')
        password=str(password).strip()
        print(f'password : {password}')
        print(f'instance : {instance}')
        
        if password is not None and instance is not None and instance.is_academy:
            print('instance :', instance)
            # Hash le nouveau mot de passe
            
            if instance.password=='not defined':
                instance.password = make_password(password)
                print('password modifié')
                print('instance_password', instance.password)
                instance.save()
                return instance
            else :
                raise serializers.ValidationError("Un mot de passe est déjà défini pour cette école")
            # Supprime la clé de connexion si présente
            # validated_data.pop('connexion_key', None)
            
            # # Met à jour les autres champs
            # for attr, value in validated_data.items():
            #     setattr(instance, attr, value)
            
            # # Sauvegarde l'instance
            # print(f"Instance  : {instance}")
        elif password is None:
            raise serializers.ValidationError("Le mot de passe est requis pour la mise à jour")
        elif not instance.is_academy:
            raise serializers.ValidationError("L'utilisateur n'est pas une école")
        
class CustomLoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    type_user=serializers.CharField()
    connexion_key=serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        type_user=attrs.get('type_user')
        connexion_key=attrs.get('connexion_key')
        
        print(f"email : {email}, password : {password}, connexion_key: {connexion_key}")

        # try:
        # # Authentification de l'utilisateur
        #     response = auth.authenticate(email=email, password=password, connexion_key=None if connexion_key==None else connexion_key, type_user=type_user) 
        #     print(f"response : {response.data}")
        #     attrs['response']=response.data
        #     return attrs
        # except Exception as e:
        #     return f"error :{e}"
        
        return attrs
   
   
class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=['id', 'email']


class AcademySerializer(serializers.ModelSerializer):
    class Meta:
        model=Academy 
        fields=['id','academy','user_id']
        
class AcademyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Academy
        fields=['academy','email']


class TeacherSerializer(serializers.ModelSerializer):
    
    # username=serializers.CharField(source='User.username')
    # subject=serializers.CharField(source='subject.name', read_only=True)
    
    # Champs des relations (tous en lecture seule car ils viennent de la DB) alors read_only=True
    
    subject_id = serializers.IntegerField(source='subject.id', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_category = serializers.CharField(source='subject.category', read_only=True)
    level_id = serializers.IntegerField(source='level.id', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    level_series = serializers.CharField(source='level.series', read_only=True)
    level_group = serializers.CharField(source='level.group', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True, allow_null=True)
    
    
    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'academy', 
            'subject_id',
            'subject_name',
            'subject_category',
            'level_id',
            'level_name',
            'level_series',
            'level_group',
            'user_id',
            'coefficient',
            'starting_year_in_academy',
            'title',
            'level_key',
        ]
        
class GenerateTeacherKeySerializer(serializers.ModelSerializer):
    class Meta :
        model = Teacher
        fields=['academy', 'subject', 'level', 'coefficient']

    def create(self, validated_data):
        try:
            level_key=GenerateTeacherKeySerializer.generate_level_key()
            validated_data['level_key']=level_key
        
            teacher=Teacher.objects.create(**validated_data)
        
            return teacher
        except Exception as e:
            print(f"{e}")
            raise serializers.ValidationError(f"Une erreur s'est produite : {e}")
        
        
    @staticmethod
    def generate_level_key():
        level_key=''.join(random.choices(string.digits, k=6))
        while Teacher.objects.filter(level_key=level_key).exists():
            level_key=''.join(random.choices(string.digits, k=6))
        return level_key

# class TutorSerializer(serializers.ModelSerializer):

#     student_key=serializers.CharField(source='student.student_key', read_only=True)    
    
#     class Meta:
#         model=Tutor
#         fields=['last_name', 'first_name','student', 'student_key', 'connexion_key']
    