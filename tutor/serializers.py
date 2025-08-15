from .models import Tutor 
from rest_framework import serializers

class ProfilTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tutor
        fields='__all__'
        
    def validate(self, attrs):
        if not attrs.get('first_name'):
            raise serializers.ValidationError("Le nom est requis")
        if not attrs.get('last_name'):
            raise serializers.ValidationError("Le prénom est requis")
        if not attrs.get('email'):
            raise serializers.ValidationError("L'email est requis")
        if not attrs.get('phone_number'):
            raise serializers.ValidationError("Le numéro de téléphone est requis")
        return super().validate(attrs)