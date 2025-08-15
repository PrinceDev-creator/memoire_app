from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields='__all__'
        
    
    def validate(self, attrs):
        pseudo=attrs['pseudo']
        school=attrs['school']
        if Subject.objects.filter(pseudo=pseudo,school=school).exists():
            raise serializers.ValidationError('Ce pseudo existe déjà pour une matière, veuillez choisir un autre')        
        return super().validate(attrs)
    
    def validate_pseudo(self, value):
        print(f'value : {value}')
        if not value:
            raise serializers.ValidationError("Le pseudo de la matière est requis.")
        elif len(value) > 3:
            print(f'len(value) : {len(value)}')
            raise serializers.ValidationError("Le pseudo de la matière doit contenir au max 3 caractères.")
        return value
        