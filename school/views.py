from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SchoolSerializer
from .models import School 


class SchoolViewSet(viewsets.ModelViewSet):
    queryset=School.objects.all()
    serializer_class=SchoolSerializer


def reportTest(request):
    return render(request, 'report_cards/report_cards.html')

def school_list(request):
    schools=School.objects.all()
    return render(request, 'schools/list_schools.html', {"schools": schools})

def view_school_notes(request) : 
    return render(request, 'view_school/login.html')