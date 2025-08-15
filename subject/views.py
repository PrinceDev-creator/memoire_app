from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubjectSerializer
from .models import Subject
from animation.models import Animation

class AdminSubjectViewSet(viewsets.ModelViewSet):
    # permission_classes=[IsAuthenticated,]
    serializer_class=SubjectSerializer
    
    def get_queryset(self):
        school= self.request.GET.get('school')
        if school:
            return Subject.objects.filter(school_id=school)
        return Subject.objects.all()
    
    
class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Subject.objects.all()
    # permission_classes=[IsAuthenticated,]
    serializer_class=SubjectSerializer
    
class SubjectsLevelView(APIView):
    def get(self,request):
        level_id=request.GET.get('level')
        infos={}
        list_subjects=[]
        animations=Animation.objects.filter(level_id=level_id)
        
        for animation in animations :
            infos={
                'subject_id': animation.subject.id,
                'subject_name' : animation.subject.name,
                'subject_pseudo': animation.subject.pseudo,
                'category': animation.subject.category,
                'coefficient': animation.coefficient
            }
            list_subjects.append(infos)
            
        return Response(list_subjects,status=200)
    
class SubjectsSchoolView(APIView):
    def get(self,request):
        school_id=request.GET.get('school')
        infos={}
        list_subjects=[]
        animations=Animation.objects.filter(school_id=school_id)
        
        for animation in animations :
            infos={
                'id': animation.subject.id,
                'name' : animation.subject.name,
                'category': animation.subject.category,
                'coefficient': animation.coefficient
            }
            list_subjects.append(infos)
            
        return Response(list_subjects,status=200)