from rest_framework.exceptions import ValidationError

from animation.models import Animation
from .models import Follow
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from students.models import Student
from tutor.models import Tutor
from level.models import Level

User=get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    
    student_key=serializers.CharField(required=False, allow_blank=True)
    tutor_key=serializers.CharField(required=False, allow_blank=True)
    student_first_name=serializers.CharField(source='student.first_name', read_only=True)
    student_last_name=serializers.CharField(source='student.last_name', read_only=True)
    tutor_first_name=serializers.CharField(source='tutor.first_name', read_only=True)
    tutor_last_name=serializers.CharField(source='tutor.last_name', read_only=True)
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all(), required=False)
    level_name = serializers.CharField(source='level.name', read_only=True)
    level_group= serializers.CharField(source='level.group', read_only=True)
    level_series= serializers.CharField(source='level.series', read_only=True)
    list_subjects=serializers.SerializerMethodField()
    school_name = serializers.CharField(source='level.school.school_name', read_only=True)
    student_registration_number=serializers.CharField(source='student.registration_number',read_only=True)
    tutor_con_key= serializers.CharField(source='tutor.user.connexion_key', read_only=True)
    
    class Meta :
        model=Follow
        fields=['student', 'student_key','student_first_name','student_last_name','student_registration_number','tutor','tutor_key','tutor_con_key','tutor_first_name','tutor_last_name' ,'level','level_name','level_group','level_series','list_subjects','school_name','academic_year']
        
        
    def get_list_subjects(self, obj):
        animations = Animation.objects.filter(level=obj.level)
        print('subjects : ', animations)
        return [{'subject_id': anim.subject.id, 'subject_name': anim.subject.name} for anim in animations]
    
    
    def validate_student_key(self, attrs):
        print(f'attrs : {attrs}')
        student_key=attrs
        if Student.objects.filter(student_key=student_key).exists():
            return student_key
        else :
            raise serializers.ValidationError('Cet étudiant n\'existe pas')
        
    def validate_tutor_key(self,attrs):
        print(f'attrs : {attrs}')
        tutor_key=attrs
        
        if User.objects.filter(connexion_key=tutor_key).exists():
            return tutor_key
        else :
            raise serializers.ValidationError('Aucun parent/tuteur avec cette clé trouvé')
        
       
    def validate_level(self, attrs):
        print(f'attrs : {attrs}')
        level=attrs
        
        if Level.objects.filter(pk=level.id).exists():
            return level
        else :
            raise serializers.ValidationError('Aucune classe trouvée')
        
        
    def validate(self,attrs):
        print(f'attrs : {attrs}')
        student_key=attrs.get('student_key')
        tutor_key=attrs.get('tutor_key')
        academic_year=settings.ACADEMIC_YEAR
        
        student=Student.objects.filter(student_key=student_key).first()
        user=User.objects.filter(connexion_key=tutor_key).first()
        tutor=Tutor.objects.filter(user=user).first()
        
        if Follow.objects.filter(tutor=tutor, student=student, academic_year=academic_year).exists():
            raise serializers.ValidationError('Cette relation existe déjà pour cette année académique')
        else : 
            return attrs
        
    
    def create(self, validated_data):
        
        student_key=validated_data.get('student_key')
        tutor_key=validated_data.get('tutor_key')
        level=validated_data.get('level')
        academic_year=settings.ACADEMIC_YEAR
        registration_number=validated_data.get('registration_number')
        
        
        print(f'academic_year : {academic_year}')
        
        student=Student.objects.filter(student_key=student_key).first()
        user=User.objects.filter(connexion_key=tutor_key).first()
        tutor=Tutor.objects.filter(user=user).first()
        
        follow=Follow.objects.create(student=student, tutor=tutor, level=level, academic_year=academic_year, registration_number=registration_number)
        
        return follow
    
    def update(self, instance, validated_data):
        student_key=validated_data['student_key']

class FollowAssignLevelSerializer(serializers.ModelSerializer):
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    registration_number = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Follow
        fields = ['level', 'student', 'academic_year', 'registration_number']

    def validate(self, attrs):
        student = attrs.get('student')
        level = attrs.get('level')
        academic_year = attrs.get('academic_year', settings.ACADEMIC_YEAR)
        print('attrs:', attrs)

        # Vérifie si l'élève a déjà une classe pour cette année académique
        if Follow.objects.filter(student=student, academic_year=academic_year).exists():
            raise serializers.ValidationError('Cet élève a déjà une classe qui lui est affectée lors de cette année académique.')
        # Vérifie si la classe existe (optionnel car le queryset le fait déjà)
        if not Level.objects.filter(pk=level.id).exists():
            raise serializers.ValidationError('Aucune classe trouvée.')
        attrs['academic_year'] = academic_year  # Ajoute l'année académique si absente
        return attrs

    def create(self, validated_data):
        # S'assure que l'année académique est bien définie
        print('validated_data:', validated_data)
        if 'academic_year' not in validated_data or not validated_data['academic_year']:
            validated_data['academic_year'] = settings.ACADEMIC_YEAR
        print(f"Creating follow with data: {validated_data}")
        follow = Follow.objects.create(**validated_data)
        return follow

    def update(self, instance, validated_data):
        level = validated_data.get('level')
        academic_year = validated_data.get('academic_year', settings.ACADEMIC_YEAR)
        # Vérifie si la relation existe déjà
        if Follow.objects.filter(student=instance.student, level=level, academic_year=academic_year).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("Cette relation existe déjà pour cette année académique.")
        instance.level = level
        instance.academic_year = academic_year
        if 'registration_number' in validated_data:
            instance.registration_number = validated_data['registration_number']
        instance.save()
        return instance

    
class AssociateTutorToStudentSerializer(serializers.ModelSerializer):
    
    tutor_key=serializers.CharField(max_length=100, write_only=True)
    student_key=serializers.CharField(max_length=100, write_only=True)
    
    class Meta:
        fields=['student', 'tutor_key', 'student_key','tutor', 'level','academic_year']
        model=Follow
    
    def validate(self, attrs):
        tutor_key=attrs.get('tutor_key')
        
        print(f'tutor_key : {tutor_key}')
        if not tutor_key:
            raise ValidationError('La clé de connexion de l\'enseignant est requise')
        if not isinstance(tutor_key, str):
            raise ValidationError('La clé de connexion de l\'enseignant doit être une chaîne de caractères')
        if len(tutor_key) != 10:    
            raise ValidationError('La clé de connexion de l\'enseignant doit contenir 10 caractères')
        if not all(c.isalnum() for c in tutor_key):
            raise ValidationError('La clé de connexion de l\'enseignant doit contenir uniquement des caractères alphanumériques')
        if not Tutor.objects.filter(user__connexion_key=tutor_key).exists():
            raise ValidationError('La clé de connexion de l\'enseignant n\'est pas valide')
        # Vérification de l'existence de l'enseignan
        
        if Tutor.objects.filter(user__connexion_key=tutor_key).exists():
            return attrs
        else :
            raise ValidationError('La clé de connexion de l\'enseignant n\'est pas valide')
        
    def update(self, instance, validated_data):
        
        try: 
            tutor_key=validated_data['tutor_key']
            print('tutor_key',tutor_key)
            tutor_key=str(tutor_key).strip()
            tutor=Tutor.objects.filter(user__connexion_key=tutor_key).first()
            if Follow.objects.filter(student=instance.student, tutor=tutor, academic_year=settings.ACADEMIC_YEAR).exists():
                raise ValidationError('Cette relation existe déjà pour cette année académique.')
            elif not tutor:
                raise ValidationError('Le parent/tuteur associé n\'existe pas.')
            instance.tutor=tutor
            instance.save()
            
            return instance
            
        except Exception as e:
            raise ValidationError(f'Une erreur s\'est produite : {str(e)}')

    
        
        
        
    