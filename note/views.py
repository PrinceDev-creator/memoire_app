from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg,Q
from .serializers import NoteSerializer
from .models import Note
from students.models import Student
from subject.models import Subject
import numpy as np
import pandas as pd


class AdminNotesViewSet(viewsets.ModelViewSet):
    queryset=Note.objects.all()
    serializer_class=NoteSerializer


class NoteViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes=[IsAuthenticated,]
    serializer_class=NoteSerializer
    
    def get_queryset(self):
        queryset=Note.objects.all()
        
        # filter_fields=['student_id','teacher_id','level_id','subject_id', 'quiz', 'cycle']
        # dict_fields_exists=dict()
        student_id=self.request.GET.get('student')
        teacher_id=self.request.GET.get('teacher')
        level_id=self.request.GET.get('level')
        subject_id=self.request.GET.get('subject')
        quiz=self.request.GET.get('quiz')
        cycle=self.request.GET.get('cycle')
        
        if student_id is not None:
            queryset=queryset.filter(student_id=student_id)
        elif teacher_id is not None:
            queryset=queryset.filter(teacher_id=teacher_id)
        elif level_id is not None:
            queryset=queryset.filter(level_id=level_id)
        elif subject_id is not None:
            queryset=queryset.filter(subject_id=subject_id)
        elif quiz is not None:
            queryset=queryset.filter(quiz=quiz)
        elif cycle is not None:
            queryset=queryset.filter(cycle=cycle)
        return queryset               
    
    # @action(detail=False, methods=['post'], url_path='notes/add')
    # def add_note(self, request, pk=None):
    #     """
    #     Ajoute une note pour un étudiant spécifique.
    #     """
    #     try:
    #         student = get_object_or_404(Student, pk=pk)
    #         subject_id = request.data.get('subject')
    #         score = request.data.get('score')
    #         level = request.data.get('level')
    #         cycle = request.data.get('cycle')

    #         if not subject_id or not score or not level or not cycle:
    #             return Response({"error": "Tous les champs (subject, score, level, cycle) sont obligatoires."},)

    #         subject = get_object_or_404(Subject, pk=subject_id)

    #         # Création de la note
    #         note = Note.objects.create(
    #             student=student,
    #             subject=subject,
    #             score=score,
    #             level=level,
    #             cycle=cycle
    #         )

    #         # Sérialisation et réponse
    #         serializer = NoteSerializer(note)
    #         return Response(serializer.data)

    #     except Exception as e:
    #         return Response({"error": str(e)})

class StudentStatisticsView(APIView):
    def get(self,request):
        
        notes_queryset=Note.objects.all()
        
        student=self.request.GET.get('student')
        subject=self.request.GET.get('subject')
        level=self.request.GET.get('level')
        quiz=self.request.GET.get('quiz')
        cycle=self.request.GET.get('cycle')
        
        request_fields={
            "student": student,
            "subject" :subject,
            "level" : level,
            "quiz":quiz,
            "cycle": cycle
        }
        
        for key,value in request_fields.items() :
            if value is not None:
                if key=='student' : 
                    notes_queryset=notes_queryset.filter(student_id=value)
                elif key=='subject' is not None:
                    notes_queryset=notes_queryset.filter(subject=value)
                elif key=='level' is not None:
                    notes_queryset=notes_queryset.filter(level=value)
                elif key=='quiz' is not None:
                    notes_queryset=notes_queryset.filter(quiz=value)
                elif key=='cycle':
                    notes_queryset=notes_queryset.filter(cycle=value)
                
        print(notes_queryset.query)
        
        if not notes_queryset.exists():
            return Response({"message" : "Aucune note trouvée"}, status=status.HTTP_404_NOT_FOUND)
        
        notes = list(notes_queryset.values_list('score', flat=True))
        
        df = pd.DataFrame(notes, columns=['score'])
        
        df['score']=df['score'].apply(lambda x: float(x) if pd.notna(x) else 0)
        
        average=df['score'].mean()
        median=df['score'].median()
        mode=df['score'].mode().to_list()
        minimum=df['score'].min()
        maximum=df['score'].max()
        ecart_type=df['score'].std()
        variance=df['score'].var()
        amplitude=maximum-minimum
        
        stats={
            "notes" : notes if len(notes)  > 0 else None,
            "moyenne" : round(average,2) if not np.isnan(average) else None,
            "mediane": round(median, 2) if not np.isnan(median) else None,
            "mode": mode if len(mode) > 0 else None,
            "minimum": round(minimum, 2) if not np.isnan(minimum) else None,
            "maximum": round(maximum, 2) if not np.isnan(maximum) else None,
            "ecart_type": round(ecart_type, 2) if not np.isnan(ecart_type) else None,
            "variance": round(variance, 2) if not np.isnan(variance) else None,
            "amplitude": round(amplitude, 2) if not np.isnan(amplitude) else None,
        }
        
        return Response(stats, status=status.HTTP_200_OK)
        
        