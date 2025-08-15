import random
import string
from level.models import Level
from subject.models import Subject
from teacher.models import Teacher
from .models import Animation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User=get_user_model()

class AddLevelSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Animation
        
        
    def validate_level(self, value):
        if not value:
            raise ValidationError('Le niveau est requis.')
        elif not Level.objects.filter(id=value.id).exists():
            raise ValidationError('Le niveau spécifié n\'existe pas.')
        return value
    
    def validate_subject(self, value):
        if not value:
            raise ValidationError('La matière est requise.')
        elif not Subject.objects.filter(id=value.id).exists():
            raise ValidationError('La matière spécifiée n\'existe pas.')
        return value
    
    def validate_coefficient(self, value):
        if value is None:
            raise ValidationError('Le coefficient est requis.')
        elif not isinstance(value, int) or value <= 0:
            raise ValidationError('Le coefficient doit être un nombre entier positif.')
        return value

    
    def validate(self, attrs): 
        level=attrs.get('level')
        subject=attrs.get('subject')
        coefficient=attrs.get('coefficient')
        
        if not level:
            raise ValidationError('Le niveau est requis.')
        if not subject:
            raise ValidationError('La matière est requise.')
        if not coefficient:
            raise ValidationError('Le coefficient est requis.')
        
        return attrs
        
    def create(self, validated_data):
        try :
            level=validated_data.get('level')
            subject=validated_data.get('subject')
            validated_data['school']=level.school
            validated_data['animation_key']=self.generate_connexion_key()
            
            print(f'level : {level} , subject : {subject} , school : {validated_data['school']}')
            
            if not self.verify_existence_of_level_subject(level.id, subject.id):
                animation=Animation.objects.create(**validated_data)
                return animation
            else:
                raise ValidationError('Cette association existe déjà dans la base de données')
        except Exception as e:
            raise ValidationError(f'Une erreur s\'est produite : {e}')
        
    def verify_existence_of_level_subject(self, level_id,subject_id):
        is_exist=Animation.objects.filter(level_id=level_id, subject_id=subject_id).exists()    
        return is_exist
    
    def generate_connexion_key(self):
        animation_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        while Animation.objects.filter(animation_key=animation_key).exists():
            animation_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        print(animation_key)
        return animation_key
    
class AssociateTeacherToAnimationKeySerializer(serializers.ModelSerializer):
    
    teacher_key = serializers.CharField(write_only=True)
    # animation_key= serializers.CharField(write_only=True)
    school_name=serializers.CharField(source='level.school.school_name', required=False, allow_blank=True)
    school_id=serializers.CharField(source='level.school.id', required=False, allow_blank=True)
    subject_name=serializers.CharField(source='subject.name', required=False, allow_blank=True)
    level_name=serializers.CharField(source='level.name', required=False, allow_blank=True)
    level_series=serializers.CharField(source='level.series', required=False, allow_blank=True)
    level_group=serializers.CharField(source='level.group', required=False, allow_blank=True)
    teacher_name=serializers.CharField(source='teacher.first_name', required=False, allow_blank=True)
    teacher_surname=serializers.CharField(source='teacher.last_name', required=False, allow_blank=True)
    teacher_con_key=serializers.CharField(source='teacher.user.connexion_key', required=False, allow_blank=True)
    
    class Meta:
        model=Animation
        fields=['teacher_key' ,'animation_key','teacher', 'teacher_con_key','teacher_name','teacher_surname','level','level_name','level_series','level_group','subject','subject_name','coefficient','school_name','school_id']
           
    def validate(self, attrs):
        teacher_key=attrs.get('teacher_key')
        
        if User.objects.filter(connexion_key=teacher_key).exists():
            return attrs
        else :
            raise ValidationError('Clé non valide, cette clé d\'enseignant n\'existe pas')
        
    def update(self, instance, validated_data):
        try:
            teacher_key=validated_data.get('teacher_key')
            teacher_key=str(teacher_key).strip()
            
            user=User.objects.get(connexion_key=teacher_key)
            
            teacher=Teacher.objects.get(user=user)
            
            print(f'teacher : {teacher} \n instance : {instance}') 
            
            instance.teacher=teacher
            instance.save()
            
            return instance
        except Exception as e :
            raise ValidationError(f'Une erreur est survenue : {e}')
        
class AnimationSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source='level.school.school_name', required=False, allow_blank=True)
    school_id=serializers.CharField(source='level.school.id', required=False, allow_blank=True)
    subject_name=serializers.CharField(source='subject.name', required=False, allow_blank=True)
    level_name=serializers.CharField(source='level.name', required=False, allow_blank=True)
    level_series=serializers.CharField(source='level.series', required=False, allow_blank=True)
    level_group=serializers.CharField(source='level.group', required=False, allow_blank=True)
    teacher_name=serializers.CharField(source='teacher.first_name', required=False, allow_blank=True)
    teacher_surname=serializers.CharField(source='teacher.last_name', required=False, allow_blank=True)
    teacher_con_key=serializers.CharField(source='teacher.user.connexion_key', required=False, allow_blank=True)
    list_subjects_level=serializers.SerializerMethodField()
    # list_levels=serializers.SerializerMethodField()
    
    class Meta:
        model=Animation
        fields=['id','animation_key','teacher','teacher_con_key','teacher_name','teacher_surname','level','level_name','level_series','level_group','subject','subject_name','coefficient','list_subjects_level','school_name','school_id']
        
    def get_list_subjects_level(self, obj):
        animations = Animation.objects.filter(level=obj.level)
        list_subjects_level=[]
        for anim in animations:
            list_subjects=[]
            list_subjects.append({
                'subject_id': anim.subject.id,
                'subject_name': anim.subject.name,
                'coefficient': anim.coefficient
            })
            list_subjects_level.append({
                'level_id': anim.level.id,
                'level_name': anim.level.name,
                'list_subjects': list_subjects
            })
            
            return list_subjects_level
        
    def get_list_levels(self, obj):
        levels = Level.objects.filter(school=obj.level.school)
        return [{'id': level.id, 'name': level.name} for level in levels]