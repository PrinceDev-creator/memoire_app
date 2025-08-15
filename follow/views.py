import traceback
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from students.models import Student
from .serializers import AssociateTutorToStudentSerializer, FollowSerializer
from .models import Follow
from rest_framework import status
from .models import Follow
from .serializers import FollowAssignLevelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class FollowViewSet(viewsets.ModelViewSet):
    
    serializer_class=FollowSerializer
    
    def get_queryset(self):
        queryset=Follow.objects.all()
        level_id=self.request.GET.get('level')
        student_id=self.request.GET.get('student')
        academic_year=self.request.GET.get('academic_year')
        
        if level_id and student_id is None and academic_year is None:
            queryset=Follow.objects.filter(level_id=level_id, academic_year=settings.ACADEMIC_YEAR)
        elif student_id and level_id and academic_year is None:
            queryset=Follow.objects.filter(level_id=level_id, student_id=student_id, academic_year=settings.ACADEMIC_YEAR)
        elif level_id and academic_year:
            queryset=Follow.objects.filter(level_id=level_id,academic_year=academic_year)
        elif academic_year :
            queryset=Follow.objects.filter(academic_year=academic_year)
        return queryset

class AssignLevelToFollowView(APIView):
    
    def post(self,request):
        try:
           print('Raw request data:', request.data)
           serializer = FollowAssignLevelSerializer(data=request.data)
           print('Serializer initialized:', serializer)
           print('serializer data:', serializer.initial_data)
           print('serializer.is_valid():', serializer.is_valid())
        except Exception as e:
            return Response({'error': f'{str(e)}'}, status=404)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
            
    
    def patch(self, request):
        data=request.data.copy()
        student= data.get('student')
        try:
            follow = Follow.objects.get(student=student, academic_year=settings.ACADEMIC_YEAR)
        except Follow.DoesNotExist:
            return Response({'error': 'Follow not found'}, status=404)
        serializer = FollowAssignLevelSerializer(follow, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class AssociateTutorToStudentView(APIView):
    
   def patch(self, request, *args, **kwargs):
    try:
        print('Raw request data:', request.data)
        student_key = str(request.data.get('student_key', '')).strip()
        print(f'Cleaned student_key: "{student_key}"')

        # Debug 1: Vérifier tous les student_keys existants
        all_keys = list(Student.objects.values_list('student_key', flat=True))
        print(f'Keys in DB: {all_keys}')

        student = Student.objects.filter(student_key__iexact=student_key).first()
        print(f'Found student: {student}')

        if not student:
            return Response(
                {'error': f'Student not found (searched key: "{student_key}")'},
                status=404
            )

        # Debug 2: Vérifier les Follows existants
        follow = Follow.objects.filter(
            student=student,
            academic_year=settings.ACADEMIC_YEAR
        ).first()
        
        if not follow:
            return Response(
                {'error': 'No follow record for this student/academic year'},
                status=404
            )

        serializer = AssociateTutorToStudentSerializer(
            instance=follow,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            print('Validation errors:', serializer.errors)
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response(serializer.data, status=200)

    except Exception as e:
        print(f'Full error trace: {traceback.format_exc()}')  # Ajoutez import traceback
        return Response(
            {'error': f'Server error: {str(e)}'},
            status=500
        )

def follow_list(request):
    follows=Follow.objects.all()
    return render(request, 'follows/list_follows.html',{"follows" : follows})