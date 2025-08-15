from rest_framework import serializers
from .models import PreRegistration  # Replace with the actual model import*
from django.contrib.auth.hashers import make_password

class PreRegistrationSerializer(serializers.ModelSerializer):
    
    # confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = PreRegistration  # Replace with the actual model
        fields = ['school_name', 'email', 'director', 'phone_number', 'address', 'state']  # Replace with the actual fields you want to include


    def validate(self, attrs):
        # Add your validation logic here
        if not attrs.get('school_name'):
            raise serializers.ValidationError("Le nom de l'école est requis")
        if not attrs.get('director'):
            raise serializers.ValidationError("Le nom du directeur est requis")
        if not attrs.get('email'):
            raise serializers.ValidationError("L'email est requis")
        if not attrs.get('phone_number'):
            raise serializers.ValidationError("Le numéro de téléphone est requis")
        if not attrs.get('address'):
            raise serializers.ValidationError("L'adresse est requise")
        # if not attrs.get('password'):
        #     raise serializers.ValidationError("Le mot de passe est requis")
        # if len(attrs.get('password')) < 8:
        #     raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères")
        # if not any(char.isdigit() for char in attrs.get('password')):
        #     raise serializers.ValidationError("Le mot de passe doit contenir au moins un chiffre")
        # if not any(char.isalpha() for char in attrs.get('password')):
        #     raise serializers.ValidationError("Le mot de passe doit contenir au moins une lettre")
        # if not any(char in "!@#$%^&*()_+" for char in attrs.get('password')):
        #     raise serializers.ValidationError("Le mot de passe doit contenir au moins un caractère spécial")
        # if not attrs.get('password') == attrs.get('confirm_password'):
        #     raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        
        
        return super().validate(attrs)    
    
    
    def create(self, validated_data):
        # Remove the confirm_password field before saving
        # validated_data.pop('confirm_password', None)
        
        # validated_data['password'] = make_password(validated_data['password'])
        
        print(f'validated_data : {validated_data}')
        
        # Create the PreRegistration instance
        pre_registration = PreRegistration.objects.create(**validated_data)
        
        return pre_registration
    
    # def update(self, instance, validated_data):
        
    #     print(f'validated_data : {validated_data}')
        
    #     print(f'instance : {instance}')
        
    #     instance.accepted=validated_data['accepted']
        
    #     print(f"instance : {instance}")
        
    #     return instance