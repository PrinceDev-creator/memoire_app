from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Tutor
from .serializers import ProfilTutorSerializer

class ProfilTutorViewSet(viewsets.ModelViewSet):
    queryset=Tutor.objects.all()
    serializer_class=ProfilTutorSerializer

class AssociateTutorToStudent(APIView):
    
    def post(self, request):
        
        data=request.data.copy()
        

def tutor_list(request):
    tutors=Tutor.objects.all()
    return render(request, 'tutors/list_tutors.html', {'tutors': tutors})
