from .models import Teacher
from rest_framework import serializers

class ProfilTeacherSerializer(serializers.ModelSerializer):
    class Meta :
        model=Teacher
        fields='__all__'
        