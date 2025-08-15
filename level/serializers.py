from rest_framework import serializers
from school.models import School
from users.models import Academy
from .models import Level
from follow.models import Follow
from django.conf import settings

class LevelSerializer(serializers.ModelSerializer):
    
    effective=serializers.SerializerMethodField()
    
    class Meta:
        model=Level
        fields=['id','name','group','series','school','class_leader','head_teacher','effective' ]
        
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Le nom du niveau est requis.")
        return value
    
    def validate_school(self, value):
        if not value:
            raise serializers.ValidationError("L'école est requise.")
        if not isinstance(value, School):
            raise serializers.ValidationError("L'école doit être une instance de School.")
        return value

    def validate(self, attrs):
        name = attrs.get('name')
        group = attrs.get('group')
        series = attrs.get('series')
        school = attrs.get('school')
        print(f"attrs : {attrs}")
        if Level.objects.filter(name=name, group=group, series=series, school=school).exists():
            raise serializers.ValidationError("Une classe avec ce nom, groupe, série et école existe déjà.")
        
        return attrs
    
    def create(self, validated_data):
        name=validated_data.get('name')
        group=validated_data.get('group')
        series=validated_data.get('series')
        school=validated_data.get('school')
        head_teacher=validated_data.get('head_teacher')
        class_leader=validated_data.get('class_leader')
        level = Level.objects.create(
            name=name,
            group=group,
            series=series,
            school=school,
            head_teacher=head_teacher,
            class_leader=class_leader
        ) 
        return level
    
    
    def get_effective(self, obj):
        return Follow.objects.filter(level=obj, academic_year=settings.ACADEMIC_YEAR).count()
    