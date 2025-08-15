from datetime import timezone
from venv import logger
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Avg,Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from follow.models import Follow
from level.models import Level
from .serializers import NoteSerializer
from .models import Note
from students.models import Student
from subject.models import Subject
import numpy as np
import pandas as pd
import json
import re
from utils.helps import send_email_with_html_body
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO
from babel.dates import format_date
from datetime import date
from urllib.parse import urljoin
import requests

academic_year=settings.ACADEMIC_YEAR

# @receiver(post_save,sender=Note)
# def notify_parents(sender,instance, created,**kwargs):
#     if created:
#         print("enter")
        
#         student = instance.student
#         # score_details = get_score_details(instance)
        
#         # Préparation des données
#         scores = []
#         if instance.score and isinstance(instance.score, dict):
#             scores = [{'type': k, 'value': v} for k, v in instance.score.items()]
        
#         context = {
#             'student_full_name': f"{student.first_name} {student.last_name}",
#             'subject_name': instance.subject.name,
#             'current_date': datetime.now().strftime("%d/%m/%Y"),
#             'has_scores': bool(scores),
#             'scores': scores,
#         }
        
#         email="princedev317@gmail.com"
#         email_receivers=[student.tutor.email]
        
#         has_send=send_email_with_html_body(email=email, subject="Nouvelle note disponible", receivers=email_receivers, template='email/student_notes.html', context=context)

#         print(f"has_send : {has_send}")


def get_score_details(instance):
    print(f"instance : {instance}")
    # score_details= ','.join([f"{key}: {value}" for key,value in instance.score.items()]) if instance.score else "Aucune note"
    # return score_details


class AdminNotesViewSet(viewsets.ModelViewSet):
    serializer_class=NoteSerializer
    
    def get_queryset(self):
        queryset = Note.objects.all()
        
        # Récupération des paramètres
        student_id = self.request.GET.get('student')
        teacher_id = self.request.GET.get('teacher')
        level_id = self.request.GET.get('level')
        subject_id = self.request.GET.get('subject')
        score = self.request.GET.get('score')
        cycle = self.request.GET.get('cycle')
        category = self.request.GET.get('category')
        
        print(f'Params - student:{student_id}, teacher:{teacher_id}, level:{level_id}, subject:{subject_id}, cycle:{cycle}, category:{category}')

        # Conditions les plus spécifiques en premier
        if subject_id and level_id and cycle:
            print('Cas 1: subject + level + cycle')
            queryset = queryset.filter(
                animation__subject__id=subject_id,
                animation__level__id=level_id,
                academic_year=academic_year,
                cycle=cycle
            )
        elif subject_id and level_id:
            print('Cas 2: subject + level')
            queryset = queryset.filter(
                animation__subject__id=subject_id,
                animation__level__id=level_id,
                academic_year=academic_year
            )
        elif student_id:
            print('Cas 3: student')
            queryset = queryset.filter(student_id=student_id, academic_year=academic_year)
        elif teacher_id:
            print('Cas 4: teacher')
            queryset = queryset.filter(animation__teacher__id=teacher_id, academic_year=academic_year)
        elif level_id and category:
            print('Cas 5: level + category')
            subject_category = Subject.objects.filter(category=category).values_list('category', flat=True)
            queryset = queryset.filter(
                animation__level__id=level_id,
                animation__subject__category=subject_category,
                academic_year=academic_year
            )
        elif level_id:
            print('Cas 6: level')
            queryset = queryset.filter(animation__level__id=level_id, academic_year=academic_year)
        elif score:
            print('Cas 7: score')
            queryset = queryset.filter(score=score, academic_year=academic_year)
        elif cycle:
            print('Cas 8: cycle')
            queryset = queryset.filter(cycle=cycle, academic_year=academic_year)

        print(f'Final queryset: {queryset.query}')
        return queryset
        
class NoteViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes=[IsAuthenticated,]
    serializer_class=NoteSerializer
    
    def get_queryset(self):
        queryset=Note.objects.all()
        
        # filter_fields=['student_id','teacher_id','level_id','subject_id', 'score', 'cycle']
        # dict_fields_exists=dict()
        student_id=self.request.GET.get('student')
        teacher_id=self.request.GET.get('teacher')
        level_id=self.request.GET.get('level')
        subject_id=self.request.GET.get('subject')
        score=self.request.GET.get('score')
        cycle=self.request.GET.get('cycle')
        
        if student_id is not None:
            queryset=queryset.filter(student_id=student_id)
        elif teacher_id is not None:
            queryset=queryset.filter(teacher_id=teacher_id)
        elif level_id is not None:
            queryset=queryset.filter(level_id=level_id)
        elif subject_id is not None:
            queryset=queryset.filter(subject_id=subject_id)
        elif score is not None:
            queryset=queryset.filter(score=score)
        elif cycle is not None:
            queryset=queryset.filter(cycle=cycle)
            
        return queryset               
    
    
class AddNoteViewSet(viewsets.ModelViewSet):
    serializer_class=NoteSerializer
    
    def get_queryset(self):
        queryset=Note.objects.all()
        
        student_id=self.request.GET.get('student')
        teacher_id=self.request.GET.get('teacher')
        level_id=self.request.GET.get('level')
        subject_id=self.request.GET.get('subject')
        score=self.request.GET.get('score')
        cycle=self.request.GET.get('cycle')
        category=self.request.GET.get('category')
        
        # print(f'level_id : {level_id}, subject_id : {subject_id}')
        
        if student_id is not None:
            print('a')
            queryset=queryset.filter(student_id=student_id)
        elif teacher_id is not None:
            print('b')
            queryset=queryset.filter(animation__teacher__id=teacher_id)
        elif level_id is not None and category is None and subject_id is None:
            print('c')
            queryset=queryset.filter(animation__level__id=level_id)
        elif subject_id is not None and level_id is None:
            print('d')
            queryset=queryset.filter(animation__subject__id=subject_id)
        elif subject_id is not None and level_id is not None:
            print('e')
            print(f'level_id : {level_id}, subject_id : {subject_id}')
            queryset=queryset.filter(animation__subject__id=subject_id, animation__level__id=level_id)
        elif score is not None:
            print('f')
            queryset=queryset.filter(score=score)
        elif cycle is not None:
            print('g')
            queryset=queryset.filter(cycle=cycle)
        elif level_id is not None and category is not None:
            print('h')
            print(f'level_id : {level_id}, category : {category}')
            queryset=queryset.filter(animation__level__id=level_id, animation__subject__category=category)
        
        return queryset  

class EditNoteViewSet(APIView):
    
    def patch(self,request):
        score = request.data.get('score')
        cycle = request.data.get('cycle')
        student = request.data.get('student')
        animation = request.data.get('animation')
        

        if not score or not cycle or not animation or not student:
            return Response({"error": "Tous les champs (note_id, score, cycle) sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            is_exists=self.verify_existence_note(student_id=student, animation=animation, cycle=cycle)
            if is_exists :
               note=Note.objects.filter(student_id=student,animation_id=animation, cycle=cycle).first()
               print('note: ', note)
            else :
               raise Exception("Cette note n'existe pas")
           
            print('instance_score: ', note.score)
            serializer = NoteSerializer(partial=True, data=request.data, instance=note)
            if serializer.is_valid():
                # Mise à jour de la note
                serializer.save()
                print('serializer.data : ', serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise Exception("Les données fournies ne sont pas valides.")

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    
    def verify_existence_note(self, student_id=None, animation=None, cycle=None):
        is_exists=Note.objects.filter(student_id=student_id, animation=animation, cycle=cycle).exists()
        print('is_existsNote : ', is_exists)
        return is_exists
        
    
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
    def get(self, request):
        student_id = request.GET.get('student')
        subject_id = request.GET.get('subject')
        level_id = request.GET.get('level')
        cycle = request.GET.get('cycle')
        scores = request.GET.get('scores')
        academic_year = settings.ACADEMIC_YEAR

        # Nettoyage des paramètres
        student_id = student_id or None
        subject_id = subject_id or None
        level_id = level_id or None
        cycle = cycle or None
        scores=scores or None
        print('scores :', scores)
        print('student ',student_id , ' subject :', subject_id, ' level :', level_id, ' cycle :', cycle, ' academic_year :', academic_year)

        # Filtrage des notes
        notes_queryset = self.filter_notes(student_id, subject_id, level_id, cycle, academic_year)
        print('notes_queryset : ', notes_queryset)
        
        list_score_data=[]
        matieres = {}
        score_data = {}
        
        for note in notes_queryset:
            try:
                # Parsing du JSON des notes
                if isinstance(note.score, str):
                    score_data = json.loads(note.score.replace("'", '"'))
                else:
                    score_data = note.score
                list_score_data.append({note.cycle: score_data})
                print(f'list_score_data : {list_score_data}')
            #     if not isinstance(score_data, dict):
            #         continue
            #     # if scores:
            #     #     scores=int(scores)
            #     #     print(f"scores :{scores} , type : {type(scores)}")
            #     #     return Response(score_data, status=status.HTTP_200_OK)
            #     # print(f"score_data : {score_data}\n")
            
            #     # Initialisation de la structure pour une nouvelle matière
            #     if subject_id is None and note.animation.subject.id not in matieres:
            #         subject_id_note=note.animation.subject.id
            #         matieres[subject_id_note] = {
            #             'nom': note.animation.subject.name,
            #             'coefficient': note.animation.coefficient,
            #             'devoirs': [],
            #             'interrogations': [],
            #             'examens': []
            #         }
                    
            #         print(f"matieresInit : {matieres}")

            #     # Classement des notes par type d'évaluation
            #     for eval_type, note_value in score_data.items():
            #         try:
            #             print(f"eval_type : {eval_type} --- note_value : {note_value}")
            #             note_float = float(note_value)
            #             # eval_type_clean = eval_type.lower().strip()

            #             # Vérification du type d'évaluation avec différentes méthodes
            #             if subject_id is None:
            #                 subject_id_mat=note.animation.subject.id
            #             else:
            #                 subject_id_mat=subject_id
            #             if self.is_devoir(eval_type):
            #                 matieres[subject_id_mat]['devoirs'].append(note_float)
            #             elif self.is_interrogation(eval_type):
            #                 matieres[subject_id_mat]['interrogations'].append(note_float)
            #             # elif self.is_examen(eval_type_clean):
            #             #     matieres[note.subject_id]['examens'].append(note_float)

            #             print(f"matieres : {matieres}")
            #         except (ValueError, TypeError):
            #             continue

            except (json.JSONDecodeError, AttributeError, ValueError) as e:
                continue
            
        if scores:
            scores=int(scores)
            print(f"scores :{scores} , type : {type(scores)}")
            print(f"list_score_data : {list_score_data}")
            return Response(list_score_data, status=status.HTTP_200_OK)
            #print(f"score_data : {score_data}\n")

            
            # if not matieres:
            #     return Response({"message": "Aucune note valide trouvée"}, exception= True, status=status.HTTP_404_NOT_FOUND)

        
        # Récupération des informations supplémentaires
        print('student_id :', student_id)
        student_info = get_student_info(student_id) if student_id else {}
        level_info = get_level_info(level_id) if level_id else {}
        category_subject = get_subject_category(subject_id) if subject_id else None

        if not notes_queryset.exists():
            return Response({}, status=status.HTTP_200_OK)

        # Traitement des scores si demandé
        if scores:
            list_score_data = self.extract_score_data(notes_queryset)
            return Response(list_score_data, status=status.HTTP_200_OK)

        # Organisation des notes par matière
        matieres = self.organize_notes_by_subject(notes_queryset, subject_id)

        if not matieres:
            return Response({"message": "Aucune note valide trouvée"}, status=status.HTTP_404_NOT_FOUND)

        # Calcul des moyennes
        moyennes_matieres, moyenne_generale, somme_coefficients = self.calculate_averages(matieres)

        # Calcul du rang si nécessaire
        rank = None
        if student_id:
            rank = self.calculate_student_rank(student_id, level_id, academic_year, subject_id)

        # Préparation de la réponse finale
        response_data = {
            **student_info,
            **level_info,
            'category_subject': category_subject,
            'subject_id': subject_id,
            "academic_year": academic_year,
            'moyennes_par_matiere': moyennes_matieres,
            'moyenne_generale': round(float(moyenne_generale), 2),
            'total_coefficients': somme_coefficients,
            'rank': self.format_rank(rank) if rank is not None else None,
            'statut': 'success' if moyenne_generale >= 10 else 'deny'
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def filter_notes(self, student_id=None, subject_id=None, level_id=None, cycle=None, academic_year=None):
        """Filtre les notes selon les paramètres fournis"""
        # notes_queryset = Note.objects.filter(academic_year=academic_year)
        
        # if student_id:
        #     notes_queryset = notes_queryset.filter(student_id=student_id)
        # if subject_id:
        #     notes_queryset = notes_queryset.filter(animation__subject__id=subject_id)
        # if level_id:
        #     notes_queryset = notes_queryset.filter(animation__level__id=level_id)
        # if cycle:
        #     notes_queryset = notes_queryset.filter(cycle=cycle)
        
        notes_queryset = Note.objects.all()
        category_subject = None
        
        # Les cas les plus spécifiques en premier
        if student_id and level_id and subject_id and cycle:
            # Cas 1 : Tous les paramètres présents
            notes_queryset = notes_queryset.filter(
                student_id=student_id,
                animation__subject__id=subject_id,
                animation__level__id=level_id,
                academic_year=academic_year,
                cycle=cycle
            )
        elif student_id and level_id and subject_id:
            # Cas 2 : student, level, subject
            notes_queryset = notes_queryset.filter(
                student_id=student_id,
                animation__subject__id=subject_id,
                animation__level__id=level_id,
                academic_year=academic_year
            )
        elif student_id and level_id and cycle:
            # Cas 2 : student, level, subject
            print('filtering by student, level, cycle, academic_year', student_id, level_id, cycle, academic_year)
            notes_queryset = notes_queryset.filter(
                student_id=student_id,
                cycle=cycle,
                animation__level__id=level_id,
                academic_year=academic_year
            )
        elif student_id and level_id:
            # Cas 3 : student, level
            notes_queryset = notes_queryset.filter(
                student_id=student_id,
                animation__level__id=level_id,
                academic_year=academic_year
            )
        elif student_id:
            # Cas 4 : student seul
            notes_queryset = notes_queryset.filter(
                student_id=student_id,
                academic_year=academic_year
            )
        elif subject_id and level_id and cycle:
            # Cas 5 : subject, level, cycle
            notes_queryset = notes_queryset.filter(
                animation__subject__id=subject_id,
                animation__level__id=level_id,
                academic_year=academic_year,
                cycle=cycle
            )
            category_subject = Subject.objects.filter(id=subject_id).values_list('category', flat=True).first()
        elif subject_id and level_id:
            # Cas 6 : subject, level
            notes_queryset = notes_queryset.filter(
                animation__subject__id=subject_id,
                animation__level__id=level_id,
                academic_year=academic_year
            )
            category_subject = Subject.objects.filter(id=subject_id).values_list('category', flat=True).first()
        elif subject_id:
            # Cas 7 : subject seul
            notes_queryset = notes_queryset.filter(
                animation__subject__id=subject_id,
                academic_year=academic_year
            )
        elif level_id:
            # Cas 8 : level seul
            notes_queryset = notes_queryset.filter(
                animation__level__id=level_id,
                academic_year=academic_year
            )
        elif cycle:
            # Cas 9 : cycle seul
            notes_queryset = notes_queryset.filter(
                cycle=cycle,
                academic_year=academic_year
            )
        else:
            # Cas par défaut : aucun filtre
            notes_queryset = notes_queryset.filter(academic_year=academic_year)

            
        return notes_queryset

    # def get_student_info(self, student_id):
    #     """Récupère les informations de l'étudiant"""
    #     student = Student.objects.filter(id=student_id).first()
    #     return {
    #         'student_first_name': student.first_name if student else None,
    #         'student_last_name': student.last_name if student else None,
    #         'registration_number': student.registration_number if student else None
    #     }

    # def get_level_info(self, level_id):
    #     """Récupère les informations du niveau"""
    #     level = Level.objects.filter(id=level_id).first()
    #     return {
    #         'level_name': level.name if level else None,
    #         'level_group': level.group if level else None,
    #         'level_series': level.series if level else None,
    #         'school_name': level.school.school_name if level and level.school else None
    #     }

    # def get_subject_category(self, subject_id):
    #     """Récupère la catégorie d'une matière"""
    #     subject = Subject.objects.filter(id=subject_id).first()
    #     return subject.category if subject else None

    def extract_score_data(self, notes_queryset):
        """Extrait les données de score brutes"""
        list_score_data = []
        for note in notes_queryset:
            try:
                score_data = json.loads(note.score.replace("'", '"')) if isinstance(note.score, str) else note.score
                list_score_data.append({note.cycle: score_data})
            except (json.JSONDecodeError, AttributeError, ValueError):
                continue
        return list_score_data

    def organize_notes_by_subject(self, notes_queryset, subject_id):
        """Organise les notes par matière"""
        matieres = {}
        
        if subject_id:
            subject = Subject.objects.filter(id=subject_id).first()
            if subject:
                matieres[subject_id] = {
                    'nom': subject.name,
                    'coefficient': 1,  # Valeur par défaut
                    'devoirs': [],
                    'interrogations': [],
                    'examens': []
                }

        for note in notes_queryset:
            try:
                score_data = json.loads(note.score.replace("'", '"')) if isinstance(note.score, str) else note.score
                if not isinstance(score_data, dict):
                    continue

                subject_id_note = note.animation.subject.id
                if subject_id is None and subject_id_note not in matieres:
                    matieres[subject_id_note] = {
                        'nom': note.animation.subject.name,
                        'coefficient': note.animation.coefficient,
                        'devoirs': [],
                        'interrogations': [],
                        'examens': []
                    }

                subject_key = subject_id or subject_id_note
                for eval_type, note_value in score_data.items():
                    try:
                        note_float = float(note_value)
                        if self.is_devoir(eval_type):
                            matieres[subject_key]['devoirs'].append(note_float)
                        elif self.is_interrogation(eval_type):
                            matieres[subject_key]['interrogations'].append(note_float)
                    except (ValueError, TypeError):
                        continue

            except (json.JSONDecodeError, AttributeError, ValueError):
                continue

        return matieres

    def calculate_averages(self, matieres):
        """Calcule les moyennes par matière et la moyenne générale"""
        moyennes_matieres = []
        somme_ponderee = 0
        somme_coefficients = 0

        for matiere_id, data in matieres.items():
            moy_interros = np.mean(data['interrogations']) if data['interrogations'] else 0
            note_devoir = data['devoirs'] if data['devoirs'] else 0

            note_matiere = (moy_interros + sum(note_devoir)) / (1 + len(note_devoir)) if note_devoir != 0 else moy_interros

            somme_ponderee += note_matiere * data['coefficient']
            somme_coefficients += data['coefficient']

            moyennes_matieres.append({
                'matiere': data['nom'],
                'coefficient': data['coefficient'],
                'moyenne_interrogations': round(float(moy_interros), 2),
                'moyenne_matiere': round(float(note_matiere), 2),
                'details': {
                    'devoirs': data['devoirs'] if data['devoirs'] else None,
                    'interrogations': data['interrogations'],
                }
            })

        moyenne_generale = somme_ponderee / somme_coefficients if somme_coefficients != 0 else 0

        return moyennes_matieres, moyenne_generale, somme_coefficients

    def calculate_student_rank(self, student_id, level_id, academic_year, subject_id=None,cycle=None):
        """Calcule le rang de l'étudiant dans sa classe ou dans une matière spécifique"""
        # Récupérer tous les étudiants du niveau
        student_id_precised = int(student_id)
        students_ids = Follow.objects.filter(level_id=level_id).values_list('student', flat=True)
        print('students_calfonc',students_ids)
        student_ranks = []
        
        for student_id in students_ids:
            # Filtrer les notes selon les mêmes critères que la vue principale
            print('student',student_id, 'type', type(student_id))
            params = {
                'student_id': student_id,
                'level_id': level_id,
                'cycle' : cycle if cycle else None,
                'academic_year': academic_year
            }
            
            if subject_id:
                params['subject_id'] = subject_id
                
            notes_queryset = self.filter_notes(**params)
            matieres = self.organize_notes_by_subject(notes_queryset, subject_id)
            
            if not matieres:
                continue
                
            # Calculer la moyenne de l'étudiant
            _, moyenne, _ = self.calculate_averages(matieres)
            student_ranks.append({
                'student_id': student_id,
                'moyenne': moyenne
            })
        
        # Trier par moyenne décroissante
        student_ranks.sort(key=lambda x: x['moyenne'], reverse=True)
        print('student_ranks : ', student_ranks)
        
        # Trouver le rang de l'étudiant demandé
        for index, rank in enumerate(student_ranks, start=1):
            print('rank: ', rank)
            print('student_precised: ', student_id_precised)
            if rank['student_id'] == student_id_precised:
                print('index: ', index)
                return index
                
        return None

    def format_rank(self, rank):
        """Formate le rang avec le suffixe approprié"""
        if rank is None:
            return None
            
        if 11 <= rank <= 13:
            return f"{rank}ème"
            
        last_digit = rank % 10
        if last_digit == 1:
            return f"{rank}er"
        else:
            return f"{rank}ème"

    def is_devoir(self, eval_type):
        """Détermine si l'évaluation est un devoir"""
        eval_type_clean = eval_type.lower().strip()
        devoir_keywords = ['devoir', 'devoirs', 'homework', 'assignment', 'dm', 'devoir maison']
        return any(keyword in eval_type_clean for keyword in devoir_keywords)

    def is_interrogation(self, eval_type):
        """Détermine si l'évaluation est une interrogation"""
        eval_type_clean = eval_type.lower().strip()
        interro_keywords = ['interro', 'interrogation', 'quiz', 'test', 'qcm', 'controle']
        return any(keyword in eval_type_clean for keyword in interro_keywords)  


class StudentAverageView(APIView):
    """
    Calcule la moyenne générale en agrégeant les résultats par cycle
    URL exemple : /api/student-average/?student=39&level=100
    """

    def get(self, request):
        # 1. Récupération des paramètres
        student_id = request.GET.get('student')
        level_id = request.GET.get('level')

        if not student_id or not level_id:
            return Response(
                {"error": "Les paramètres student et level sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Récupérer les cycles disponibles pour cet étudiant
        cycles = self.get_student_cycles(student_id, level_id, academic_year)
        if not cycles:
            return Response(
                {"error": "Aucun cycle trouvé pour cet étudiant"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. Récupérer les moyennes par cycle
        cycle_averages = []
        base_url = "http://0.0.0.0:8000/statistics/"

        for cycle in cycles:
            try:
                # Construction de l'URL avec paramètres
                params = {
                    'student': student_id,
                    'level': level_id,
                    'cycle': cycle,
                }

                # Appel à l'API statistics
                response = requests.get(
                    urljoin(base_url, ""),
                    params=params,
                    timeout=3
                )
                response.raise_for_status()

                data = response.json()
                if 'moyenne_generale' in data:
                    cycle_averages.append(float(data['moyenne_generale']))

            except Exception as e:
                continue  # On ignore les cycles en erreur

        # 4. Calcul de la moyenne globale
        if not cycle_averages:
            return Response(
                {"error": "Aucune donnée valide pour calculer la moyenne"},
                status=status.HTTP_404_NOT_FOUND
            )

        global_average = np.mean(cycle_averages)
        weighted_average = self.calculate_weighted_average(cycle_averages)
        student_info=get_student_info(student_id=student_id)
        level_info=get_level_info(level_id=level_id)
        
        rank = self.calculate_student_rank(student_id, level_id, academic_year)
        
        # 5. Préparation de la réponse
        response_data = {
            **student_info,
            **level_info,
            "student_id": student_id,
            "level_id": level_id,
            "academic_year": academic_year,
            "cycles_processed": len(cycle_averages),
            "moyenne_generale": round(global_average, 2),
            "moyenne_ponderee": round(weighted_average, 2),
            "rang": {
                "position": rank,
                "forme_litterale": self.format_rank(rank) if rank else None
            },
            "detail_par_cycle": [
                {"cycle": cycle, "moyenne": avg} 
                for cycle, avg in zip(cycles, cycle_averages)
            ]
        }

        return Response(response_data)

    def get_student_cycles(self, student_id, level_id, academic_year):
        """Récupère les cycles disponibles pour un étudiant"""
        from django.db.models import Count
        from .models import Note
        
        cycles = Note.objects.filter(
            student_id=student_id,
            animation__level_id=level_id,
            academic_year=academic_year
        ).values_list('cycle', flat=True).distinct()

        return sorted(list(cycles))

    def calculate_weighted_average(self, averages):
        """Calcule une moyenne pondérée si nécessaire"""
        # Ici on pourrait implémenter une logique de pondération par cycle
        # Par défaut on retourne une simple moyenne
        return np.mean(averages)

    def calculate_student_rank(self, student_id, level_id, academic_year):
        """Calcule le rang de l'étudiant dans sa classe"""
        # 1. Récupérer tous les étudiants du même niveau
        students = Follow.objects.filter(
            level_id=level_id,
            academic_year=academic_year
        ).select_related('student')

        # 2. Calculer la moyenne générale pour chaque étudiant
        student_averages = []
        for follow in students:
            # Utilisez la même méthode que pour l'étudiant principal
            cycles = self.get_student_cycles(follow.student.id, level_id, academic_year)
            cycle_averages = []
            print('cycles :', cycles)
            
            for cycle in cycles:
               # Construction des paramètres pour la requête
                params = {
                    'student': follow.student.id,  # L'étudiant courant dans la boucle
                    'level': level_id,
                    'cycle': cycle,
                }

                try:
                    # Appel à votre endpoint interne ou méthode existante
                    response = requests.get(
                        "http://0.0.0.0:8000/statistics/",
                        params=params,
                        timeout=2
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    # Vérifie si la moyenne générale existe dans la réponse
                    if 'moyenne_generale' in data:
                        cycle_averages.append(float(data['moyenne_generale']))
                        
                except (requests.RequestException, ValueError, KeyError) as e:
                    # Log l'erreur mais continue avec les autres cycles
                    logger.warning(f"Erreur pour cycle {cycle}, étudiant {follow.student.id}: {str(e)}")
                    continue
                    
                if cycle_averages:
                    avg = np.mean(cycle_averages)
                    student_averages.append({
                        'student_id': follow.student.id,
                        'moyenne': avg
                    })
        
        print('student_averages :', student_averages)

        # 3. Trier par moyenne décroissante
        student_averages.sort(key=lambda x: x['moyenne'], reverse=True)

        # 4. Trouver le rang de l'étudiant cible
        for index, student in enumerate(student_averages, start=1):
            if student['student_id'] == int(student_id):
                return index

        return None

    def format_rank(self, rank):
        """Formate le rang en version littérale (1er, 2eme, etc.)"""
        if not rank:
            return None
            
        if 11 <= rank <= 13:
            return f"{rank}ème"
            
        last_digit = rank % 10
        if last_digit == 1:
            return f"{rank}er"
        else:
            return f"{rank}ème"


class SendReportCardAPIView(APIView):
    def post(self, request):
        student_id=request.data.get('student')
        level_id=request.data.get('level')
        cycle = request.data.get('cycle')
        academic_year = settings.ACADEMIC_YEAR
        
        try:
            # Récupérer l'étudiant et vérifier son existence
            student = Student.objects.get(id=student_id)
            level = Level.objects.get(id=level_id)
            
            # Récupérer le(s) tuteur(s) via le modèle Follow
            follows = Follow.objects.filter(
                student=student,
                level=level,
                academic_year=academic_year
            ).select_related('tutor')
            
            if not follows.exists():
                return Response(
                    {"error": "Aucun tuteur trouvé pour cet élève dans ce niveau et année scolaire"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Générer les données du bulletin
            report_data = self.generate_report_data(student_id, level_id, cycle, academic_year)
            
            # Générer le PDF
            pdf_content = self.generate_pdf_report(cycle,report_data)
            
            # Envoyer le bulletin à chaque tuteur
            for follow in follows:
                if follow.tutor and follow.tutor.user.email:
                    self.send_report_email(
                        tutor=follow.tutor,
                        student=student,
                        level=level,
                        academic_year=academic_year,
                        pdf_content=pdf_content,
                        report_data=report_data
                    )
            
            return Response(
                {"success": f"Bulletin envoyé à {follows.count()} tuteur(s)"},
                status=status.HTTP_200_OK
            )
            
        except Student.DoesNotExist:
            return Response(
                {"error": "Étudiant non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Level.DoesNotExist:
            return Response(
                {"error": "Niveau non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Une erreur est survenue: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def generate_report_data(self, student_id, level_id, cycle, academic_year):
        
        """Génère les données en appelant StudentAverageView"""
        
        # Construction de l'URL
        if cycle == 'all':
            base_url = "http://0.0.0.0:8000"
            # Mode agrégé - on appelle sans paramètre cycle
            url = urljoin(base_url, "/student-average/")
            params = {
                'student': student_id,
                'level': level_id
            }
        
            try:
                # Appel à l'API StudentAverageView
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Vérification des données reçues
                if 'moyenne_generale' not in data:
                    raise ValueError("Réponse de l'API invalide")
                
                # Formatage des données pour le template
                student = Student.objects.get(id=student_id)
                level = Level.objects.get(id=level_id)
                
                return {
                    'student': {
                        'first_name': student.first_name,
                        'last_name': student.last_name,
                        'registration_number': student.registration_number
                    },
                    'level': {
                        'name': level.name,
                        'series': level.series,
                        'group': level.group
                    },
                    'school': {
                        'name': level.school.school_name if level.school else None,
                        'address': level.school.address if level.school else None
                    },
                    'academic_year': academic_year,
                    'cycle': cycle if cycle != 'all' else 'Tous les semestres\trimestres',
                    'moyennes_par_matiere': self.format_subjects(data.get('moyennes_par_matiere', [])),
                    'moyenne_generale': data['moyenne_generale'],
                    'appreciation_generale': self.get_appreciation(data['moyenne_generale']),
                    'rang': data.get('rang', {}),
                    'detail_par_cycle': data.get('detail_par_cycle', []),
                    'date_emission': self.get_current_date()
                }
                
            except requests.RequestException as e:
                raise Exception(f"Erreur de connexion à l'API: {str(e)}")
            except (KeyError, ValueError) as e:
                raise Exception(f"Erreur dans les données de l'API: {str(e)}")


        """Génère les données statistiques pour le bulletin"""
        # Récupérer les notes de l'étudiant
        # notes_queryset = Note.objects.filter(
        #     student_id=student_id,
        #     animation__level_id=level_id,
        #     cycle=cycle,
        #     academic_year=academic_year
        # ).select_related('animation__subject', 'animation__level')
        
        # if not notes_queryset.exists():
        #     raise ValueError("Aucune note trouvée pour cet étudiant dans ce niveau et cycle.")
        # # Organiser les notes par matière
        # matieres = {}
        # for note in notes_queryset:
        #     try:
        #         score_data = json.loads(note.score.replace("'", '"')) if isinstance(note.score, str) else note.score
        #         if not isinstance(score_data, dict):
        #             continue
                
        #         subject_id = note.animation.subject.id
        #         if subject_id not in matieres:
        #             matieres[subject_id] = {
        #                 'nom': note.animation.subject.name,
        #                 'coefficient': note.animation.coefficient,
        #                 'devoirs': [],
        #                 'interrogations': [],
        #                 'examens': []
        #             }
                
        #         for eval_type, note_value in score_data.items():
        #             try:
        #                 note_float = float(note_value)
        #                 if self.is_devoir(eval_type):
        #                     matieres[subject_id]['devoirs'].append(note_float)
        #                 elif self.is_interrogation(eval_type):
        #                     matieres[subject_id]['interrogations'].append(note_float)
        #             except (ValueError, TypeError):
        #                 continue
        #     except (json.JSONDecodeError, AttributeError, ValueError):
        #         continue
        
        # # Calculer les moyennes
        # moyennes_matieres = []
        # somme_ponderee = 0
        # somme_coefficients = 0
        
        # for matiere_id, data in matieres.items():
        #     moy_interros = np.mean(data['interrogations']) if data['interrogations'] else 0
        #     note_devoir = data['devoirs'] if data['devoirs'] else 0
            
        #     note_matiere = (moy_interros + sum(note_devoir)) / (1 + len(note_devoir)) if note_devoir != 0 else moy_interros
            
        #     somme_ponderee += note_matiere * data['coefficient']
        #     somme_coefficients += data['coefficient']
            
        #     moyennes_matieres.append({
        #         'matiere': data['nom'],
        #         'coefficient': data['coefficient'],
        #         'moyenne_matiere': round(float(note_matiere), 2),
        #         'appreciation': self.get_appreciation(note_matiere)
        #     })
        
        # moyenne_generale = somme_ponderee / somme_coefficients if somme_coefficients != 0 else 0
        
        # # Récupérer les informations supplémentaires
        # student = Student.objects.get(id=student_id)
        # level = Level.objects.get(id=level_id)
        
        # Construction de l'URL
        base_url = "http://0.0.0.0:8000"
        # Mode agrégé - on appelle sans paramètre cycle
        url = urljoin(base_url, "/statistics/")
        params = {
            'student': student_id,
            'level': level_id,
            'cycle':cycle
        }
        
        try:
            # Appel à l'API StudentAverageView
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            student = Student.objects.get(id=student_id)
            level = Level.objects.get(id=level_id)
            
            # Vérification des données reçues
            if 'moyenne_generale' not in data:
                raise ValueError("Réponse de l'API invalide")
                
            # Formatage des données pour le template
            moyennes_matieres = self.format_subjects(data.get('moyennes_par_matiere', []))
            moyenne_generale = data['moyenne_generale']
            
        except requests.RequestException as e:
            raise Exception(f"Erreur de connexion à l'API: {str(e)}")
        except (KeyError, ValueError) as e:
            raise Exception(f"Erreur dans les données de l'API: {str(e)}")
        
        
        return {
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'registration_number': student.registration_number
            },
            'level': {
                'name': level.name,
                'series': level.series,
                'group': level.group
            },
            'school': {
                'name': level.school.school_name if level.school else None,
                'address': level.school.address if level.school else None
            },
            'academic_year': academic_year,
            'cycle' : cycle,
            'rang':data.get('rank', {}),
            'moyennes_par_matiere': moyennes_matieres,
            'moyenne_generale': round(float(moyenne_generale), 2),
            'appreciation_generale': self.get_appreciation(moyenne_generale),
            'date_emission':  format_date(date.today(), format='full', locale='fr'),
        }
        
    def format_subjects(self, subjects_data):
        """Formate les données des matières pour le template"""
        return [{
            'matiere': subj.get('matiere', 'Inconnu'),
            'coefficient': subj.get('coefficient', 1),
            'moyenne_matiere': subj.get('moyenne_matiere', 0),
            'appreciation': self.get_appreciation(subj.get('moyenne_matiere', 0))
        } for subj in subjects_data]

    def get_current_date(self):
        """Retourne la date formatée"""
        return format_date(date.today(), format='full', locale='fr')

    def generate_pdf_report(self, cycle, report_data):
        """Génère le PDF du bulletin à partir des données"""
        print('report_data : ', report_data)
        html_string = render_to_string('report_cards/report_card_template.html', report_data) if cycle !='all' else render_to_string('report_cards/report_card_template_moan.html', report_data)
        result = BytesIO()
        
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            return result.getvalue()
        raise Exception("Erreur lors de la génération du PDF")

    def send_report_email(self, tutor, student, level, academic_year, pdf_content, report_data):
        """Envoie le bulletin par email au tuteur"""
        subject = f"Bulletin scolaire de {student.first_name} {student.last_name} - {level.name} - {academic_year}"
        
        # Générer le contenu HTML
        email_body_html = render_to_string('report_cards/email_report_template.html', {
            'tutor': tutor,
            'student': student,
            'level': level,
            'academic_year': academic_year,
            'report_data': report_data
        })
        
        # Créer une version texte brut alternative
        email_body_text = f"""
        Bulletin scolaire de {student.first_name} {student.last_name}
        Classe: {level.name}
        Année scolaire: {academic_year}
        
        Pour consulter le bulletin, veuillez ouvrir le fichier PDF joint.
        
        Cordialement,
        L'équipe pédagogique
        """
        
        email = EmailMultiAlternatives(  # Utilisez EmailMultiAlternatives au lieu de EmailMessage
            subject,
            email_body_text,  # version texte brut
            settings.EMAIL_HOST_USER,
            [tutor.email],
        )
        
        # Attacher la version HTML
        email.attach_alternative(email_body_html, "text/html")
        
        # Attacher le PDF
        filename = f"Bulletin_{student.last_name}_{student.first_name}_{academic_year}.pdf"
        email.attach(filename, pdf_content, 'application/pdf')
        
        email.send()
        
    def get_appreciation(self, note):
        """Retourne l'appréciation correspondant à la note"""
        if note >= 18: return 'Excellent'
        if note >= 16: return 'Très bien'
        if note >= 14: return 'Bien'
        if note >= 12: return 'Assez bien'
        if note >= 10: return 'Passable'
        return 'Insuffisant'

    def is_devoir(self, eval_type):
        """Détermine si l'évaluation est un devoir"""
        eval_type_clean = eval_type.lower().strip()
        return any(keyword in eval_type_clean for keyword in ['devoir', 'devoirs', 'homework', 'assignment'])

    def is_interrogation(self, eval_type):
        """Détermine si l'évaluation est une interrogation"""
        eval_type_clean = eval_type.lower().strip()
        return any(keyword in eval_type_clean for keyword in ['interro', 'interrogation', 'quiz', 'test'])
    

#méthodes utilisées utilisées par toutes les classes

def get_student_info(student_id):
        """Récupère les informations de l'étudiant"""
        student = Student.objects.filter(id=student_id).first()
        return {
            'student_first_name': student.first_name if student else None,
            'student_last_name': student.last_name if student else None,
            'registration_number': student.registration_number if student else None
        }

def get_level_info(level_id):
    """Récupère les informations du niveau"""
    level = Level.objects.filter(id=level_id).first()
    return {
        'level_name': level.name if level else None,
        'level_group': level.group if level else None,
        'level_series': level.series if level else None,
        'school_name': level.school.school_name if level and level.school else None
    }

def get_subject_category(subject_id):
    """Récupère la catégorie d'une matière"""
    subject = Subject.objects.filter(id=subject_id).first()
    return subject.category if subject else None
