from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import StudentSerializer
from note.serializers import NoteSerializer
from subject.serializers import SubjectSerializer
from .models import Student
from subject.models import Subject
from note.models import Note
from django.db.models import Avg
from users.permissions import IsAcademyPermissions

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    # permission_classes = [IsAuthenticated,]
    serializer_class = StudentSerializer
        
    @action(detail=True, methods=['get'], url_path='notes/(?P<level>\d+)/(?P<cycle>\d+)/(?P<subject>\d+)/average')
    def average_student(self, request, pk=None, level=None, cycle=None, subject=None):
        try:
            studentcurrent = get_object_or_404(Student, pk=pk)
            subjectcurrent = get_object_or_404(Subject, pk=subject)
            
            notes = Note.objects.filter(student=studentcurrent, level=level, cycle=cycle, subject=subjectcurrent)
            
            average = notes.aggregate(average=Avg('score'))['average'] or 0
            
            results = [{
                'student': f"{studentcurrent.name}",
                'notes': [subjectcurrent.name, list(notes.values('score'))],
                'average': round(average, 2),
            }]
            return Response({'results': results})  
         
        except Student.DoesNotExist :
            return Response({"Error: Apprenant non trouvé"})
        
        except Subject.DoesNotExist :
            return Response({"Error : Matière non trouvée"})
        
        except Exception as e:
            return Response({"Error: ": str(e)})
        

class AdminStudentViewSet(viewsets.ModelViewSet):
    queryset=Student.objects.all()
    serializer_class=StudentSerializer
    # permission_classes=[IsAuthenticated, IsAcademyPermissions]
    