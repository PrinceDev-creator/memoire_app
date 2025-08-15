from django.shortcuts import render
from .serializers import ProfilTeacherSerializer
from rest_framework import viewsets
from .models import Teacher

class ProfilTeacherViewSet(viewsets.ModelViewSet):
    queryset=Teacher.objects.all()
    serializer_class=ProfilTeacherSerializer

def teacher_list(request):
    teachers=Teacher.objects.all()
    return render(request,'teachers/list_teachers.html',{'teachers': teachers})