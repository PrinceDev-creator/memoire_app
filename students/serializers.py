from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from follow.models import Follow
from level.models import Level
from .models import Student
from tutor.models import Tutor
import random, string

User=get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        exclude=['student_key']    
        
    def create(self, validated_data):
        student_key=self.generate_student_key()
        registration_number=validated_data.get('registration_number')
        validated_data['student_key']=student_key
        validated_data['registration_number']=registration_number
        
        try:
            student=Student.objects.create(**validated_data)
            return student
        except Exception as e:
            raise serializers.ValidationError(f"Une erreur s'est produite : {e}")
        
    def generate_student_key(self):
        student_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
        while Student.objects.filter(student_key=student_key).exists():
            student_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return student_key

    def detect_duplicate_registration_number(self,reg_num):
        valid_reg_num=False
        if Student.objects.filter(registration_number=reg_num).exists():
            valid_reg_num=True
        return valid_reg_num
    

class StudentFollowCreateSerializer(serializers.Serializer):
    # Champs pour Student
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    sexe = serializers.CharField()
    registration_number = serializers.IntegerField()
    # level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

    def create(self, validated_data):
        # Création du student
        validated_data['student_key'] = self.generate_student_key()
        student = Student.objects.create(**validated_data)
        # Création du follow
        Follow.objects.create(student=student,academic_year=settings.ACADEMIC_YEAR)
        return student

    def generate_student_key(self):
        student_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
        while Student.objects.filter(student_key=student_key).exists():
            student_key=''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return student_key
        
        
        
            
            
        
        
    
        
        