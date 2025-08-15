from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from follow.models import Follow
from level.models import Level
from .serializers import StudentFollowCreateSerializer, StudentSerializer
from note.serializers import NoteSerializer
from subject.serializers import SubjectSerializer
from students.serializers import StudentFollowCreateSerializer
from .models import Student
from subject.models import Subject
from note.models import Note
from django.db.models import Avg
from users.permissions import IsAcademyPermissions

class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    # permission_classes = [IsAuthenticated,]
    serializer_class = StudentSerializer     
    # @action(detail=True, methods=['get'], url_path='notes/(?P<level>\d+)/(?P<cycle>\d+)/(?P<subject>\d+)/average')
    # def average_student(self, request, pk=None, level=None, cycle=None, subject=None):
    #     try:
    #         studentcurrent = get_object_or_404(Student, pk=pk)
    #         subjectcurrent = get_object_or_404(Subject, pk=subject)
            
    #         notes = Note.objects.filter(student=studentcurrent, level=level, cycle=cycle, subject=subjectcurrent)
            
    #         average = notes.aggregate(average=Avg('score'))['average'] or 0
            
    #         results = [{
    #             'student': f"{studentcurrent.name}",
    #             'notes': [subjectcurrent.name, list(notes.values('score'))],
    #             'average': round(average, 2),
    #         }]
    #         return Response({'results': results})  
         
    #     except Student.DoesNotExist :
    #         return Response({"Error: Apprenant non trouvé"})
        
    #     except Subject.DoesNotExist :
    #         return Response({"Error : Matière non trouvée"})
        
    #     except Exception as e:
    #         return Response({"Error: ": str(e)})
        
class StudentFollowCreateView(APIView):
    def post(self, request):
        serializer = StudentFollowCreateSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({'student_id': student.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminStudentViewSet(viewsets.ModelViewSet):
    serializer_class=StudentSerializer
    
    def get_queryset(self):
        queryset=Student.objects.all()
        academy_id=self.request.GET.get("academy")
        level_id=self.request.GET.get('level')
        sexe=self.request.GET.get('sexe')
        print(f"academy : {academy_id}, level : {level_id}, sexe : {sexe}")
        if academy_id is not None and level_id is not None and sexe is None:
            queryset=Student.objects.filter(academy_id=academy_id, level_id=level_id)
        elif level_id is not None and academy_id is None and sexe is None:
            queryset=Student.objects.filter(level_id=level_id)
        elif academy_id is not None and level_id is not None and sexe is not None:
            queryset=Student.objects.filter(academy_id=academy_id, level_id=level_id, sexe = sexe)
            
        print(queryset.query) 
           
        return queryset

    # permission_classes=[IsAuthenticated, IsAcademyPermissions]
    
class LevelStudentsView(APIView):
        
    def get(self,request):
        level_id=request.GET.get('level')
        academic_year=request.GET.get('academic_year')
        if academic_year is None:
            academic_year=settings.ACADEMIC_YEAR
            
        list_students=[]
        students_ids=Follow.objects.filter(level_id=level_id,academic_year=academic_year).values_list('student',flat=True)
        print(f'students_ids : {students_ids}')
        for student_id in students_ids :
            student=Student.objects.get(pk=student_id)
            infos_student={
                'id': student.id,
                'first_name' : student.first_name,
                'last_name' :student.last_name,
                'sexe' : student.sexe,
                'registration_number' :student.registration_number #Follow.objects.filter(student=student, academic_year=settings.ACADEMIC_YEAR).values_list('registration_number', flat=True).first()
            }
            list_students.append(infos_student)
            
        return Response(list_students, status=200)

class SchoolStudentsView(APIView):
        
    def get(self,request):
        school_id=request.GET.get('school')
        list_students=[]
        students_ids=Student.objects.filter(school_id=school_id).values_list('id',flat=True)
        print(f'students_ids : {students_ids}')
        for student_id in students_ids :
            student=Student.objects.get(pk=student_id)
            associate_level=Follow.objects.filter(student_id=student.id, academic_year=settings.ACADEMIC_YEAR).exists()
            print('student_regn : ',student.registration_number)
            infos_student={
                'id': student.id,
                'first_name' : student.first_name,
                'last_name' :student.last_name,
                'sexe' : student.sexe,
                'registration_number' :  student.registration_number, 
                'student_key' : student.student_key,
                'associate_level' : associate_level
            }
            list_students.append(infos_student)
            
        return Response(list_students, status=200)


def student_list(request):
    students=Student.objects.all()
    return render(request, "students/list_students.html", {"students": students})