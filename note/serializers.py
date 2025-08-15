import json
import ast
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from school.models import School
from students.models import Student
from teacher.models import Teacher
from tutor.models import Tutor
from utils.helps import send_email_with_html_body 
from .models import Note
from follow.models import Follow
from animation.models import Animation
from django.db.models import F, Value, Func
from django.db.models.functions import Cast, JSONObject
from babel.dates import format_date
from datetime import date
import copy

User=get_user_model()
academic_year=settings.ACADEMIC_YEAR

class NoteSerializer(serializers.ModelSerializer):
    
    subject_category = serializers.CharField(source='subject.category', required=False, allow_blank=True)
    
    class Meta:
        model=Note
        fields=['score', 'cycle', 'student', 'animation', 'subject_category', 'is_validated', 'created_at', 'updated_at']
    
        
    def create(self, validated_data):
        # teacher=validated_data.get('teacher')
        # level=validated_data.get('level')
        # subject=validated_data.get('subject')
        # academy=validated_data.get('academy')
        
        # print(f"teacher : {teacher}, level : {level}, subject: {subject}, academy: {academy}")
        
        # coefficient=self.search_coeficient(teacher=teacher)
        # validated_data['coefficient']=coefficient
        
        print(f"validated_data: {validated_data}")
        added={}
        
        try:
            # is_exist=self.verify_identity_teacher(teacher=teacher, level=level, subject=subject, academy=academy) 
            student=validated_data.get('student')
            score=validated_data.get('score')
            animation=validated_data.get('animation')
            cycle=validated_data.get('cycle')
            print(f"student : {student}, animation : {animation}, cycle: {cycle}")
            student_exists=self.verify_existence_of_student(student=student)
            if student_exists:
                is_right_animation=self.verify_rightness_of_animation(animation=validated_data.get('animation'), student=validated_data.get('student'))
                print(f'is_right_animation : {is_right_animation}')
                if is_right_animation:
                    # validated_data['score']=self.parse_score(score)
                    search_note = self.search_note_of_student(student_id=student.id,animation_id=animation.id,cycle=int(cycle)) #rechercher si la note existe déjà)
                    print(f'search_note : {search_note}')
                    if search_note is None : 
                        validated_data['score']=self.parse_score(score)
                        note = Note.objects.create(**validated_data)
                        added=note.score
                        print(f"note: {note}")
                        print(f"note_score_added: {added}")
                    else :
                        note=self.search_note_of_student(student_id=student.id, animation_id=animation.id,cycle=cycle)
                        new_score=validated_data.get('score')
                        new_score=self.parse_score(new_score)
                        score_exists=self.detect_duplication_of_evaluation(student=student, score=new_score, animation=animation,cycle=cycle)
                        print(f"note_score: {new_score}")
                        print(f"score_exists: {score_exists}")

                        if not score_exists:
                            old_score=copy.deepcopy(note.score)
                            for key, value in new_score.items() : 
                                print(f'key: {key}, value: {value}')
                                note.score[key]= value
                                note.save()
                                added=self.detect_added_keys(old_grades=old_score, new_grades=new_score)
                                print(f"added: {added}")
                        else : 
                            raise serializers.ValidationError("Cette évaluation existe déjà, si vous souhaitez modifier la note, veuillez contacter l'administrateur ou l'école")
                
                print(f"note: {note}") 
                message_type= {
                    'added' : added,
                    }   
                 
                tutor=Follow.objects.filter(student=student, academic_year=academic_year).values_list('tutor', flat=True).first()
                school=Animation.objects.filter(pk=animation.id).values_list('school', flat=True).first()
                teacher_obj=Animation.objects.filter(pk=animation.id).values_list('teacher', flat=True).first()
                teacher=Teacher.objects.filter(pk=teacher_obj).first()
                
                print(f'school : {school}, teacher : {teacher}')
                print(f'tutor : {tutor}')
                
                #Envoi des notes aux parents  
                tutor_receiver=Tutor.objects.filter(pk=tutor).values_list('email',flat=True)                  
                self.notify_message(instance=note,message_type=message_type, receiver=tutor_receiver, template='emails/student_notes.html')    
                
                #Notification à l'école
                school_receiver=School.objects.filter(pk=school).values_list('email',flat=True)
                print('school_receiver: ', school_receiver)
                self.notify_message(instance=note,message_type=message_type,receiver=school_receiver,template='schools/notif_operation_notes.html')
                
                #Notification à l'enseignant
                teacher_receiver=User.objects.filter(pk=teacher.user.id).values_list('email', flat=True)
                print(f'teacher_receiver : {teacher_receiver}')
                self.notify_message(instance=note,message_type=message_type, receiver=teacher_receiver, template='teachers/notif_ajout_notes.html')
                
                return note
            else:
                raise serializers.ValidationError("L'apprenant n'existe pas")
                # raise serializers.ValidationError("Les informations de l'expéditeur sont incorrectes")
            
        except Exception as e:
            print(f"error : {e}")
            raise serializers.ValidationError("Erreur lors de l'insertion des notes, vérifier les informations saisies")
    

    def update(self, instance, validated_data):
        print('instance ', instance, ' validated_data ', validated_data)
        new_score = validated_data.get('score')
        new_score = self.parse_score(new_score)
        
        # Crée une COPIE PROFONDE du dictionnaire original
        old_score = copy.deepcopy(instance.score)
        print('old_scoreBef : ', old_score)
        
        type = ''
        changes = {}
        print(f"new_score: {new_score}")
        
        for key, value in new_score.items():
            print(f'key: {key}, value: {value}')
            instance.score[key] = value
            print(f"instance.score: {instance.score}")
        
        instance.save()
        print('old_scoreAft : ', old_score)  # Maintenant inchangé
        print('new_instance : ', instance)
        
        changes = self.compare_notes(old_grades=old_score, new_grades=new_score)
        print(f"changes: {changes}")
        
        message_type = {
            'edited': changes,
        }
        
        student= instance.student
        note=instance.note
        tutor=Follow.objects.filter(student=student, academic_year=academic_year).values_list('tutor', flat=True).first()
        print(f'tutor : {tutor}')
        
        tutor=Follow.objects.filter(student=student, academic_year=academic_year).values_list('tutor', flat=True).first()
        school=Animation.objects.filter(pk=instance.animation.id).values_list('school', flat=True).first()
          
        #Notification au parent                    
        tutor_receiver=Tutor.objects.filter(pk=tutor).values_list('email',flat=True)                  
        self.notify_message(instance=note,message_type=message_type, receiver=tutor_receiver, template='emails/student_notes.html')    
        
        #Notification à l'école
        school_receiver=School.objects.filter(pk=school).values.list('email',flat=True)
        self.notify_message(instance=note,message_type=message_type,receiver=school_receiver,template='emails/schools/notif_operation_notes.html')

        return instance
    
    def compare_notes(self,old_grades, new_grades):
        changes = {}
        print(f"old_gradesFunc: {old_grades}, new_gradesFunc: {new_grades}")
        # Vérifier les clés communes avec valeurs différentes
        for key in old_grades:
            if key in new_grades and old_grades[key] != new_grades[key]:
                changes[key] = {
                    'old': old_grades[key],
                    'new': new_grades[key]
                }
        print('changesFunc : ', changes)
        
        return changes
    
    def detect_added_keys(self,old_grades, new_grades):
        added_keys = {}
        
        for key in new_grades:
            if key not in old_grades:
                added_keys[key] = new_grades[key]  # Stocke la nouvelle clé et sa valeur
        
        return added_keys
        
    # def verify_identity_teacher(teacher):
    #     is_exist= Teacher.objects.filter(pk=teacher.id).exists()
    #     return is_exist
    
    # def search_coeficient(teacher):
    #     animation=Animation.objects.filter(teacher=teacher).first()
    #     coefficient=animation.coefficient
    #     print(f"coefficient: {coefficient}")
    #     return coefficient
    
    def verify_existence_of_student(self, student):
        return Student.objects.filter(pk=student.id).exists()
    
    def detect_duplication_of_evaluation(self, student , score, animation,cycle):
        print('detect_duplication_of_score')
        if not score :
            return False
        
        key=list(score.keys())[0] #Récupère la première clé du dictionnaire
        print(f"key: {key}")
        
        existing_scores=Note.objects.filter(student=student,animation=animation,cycle=cycle).values('score').first()['score']
        print(f"existing_scores: {existing_scores}")
        if isinstance(existing_scores,dict) and key in existing_scores:
            print(f"existing_scores: {existing_scores}")
            return True
        return False
    
    def verify_rightness_of_animation(self,animation, student): 
       """On vérifie si l'animation tapé correspond à la classe de l'apprenant"""
       print(f"animation_id: {animation.id}")
       level_follow=Follow.objects.filter(student=student, academic_year=academic_year).values_list('level',flat=True).first()
       level_animation=Animation.objects.filter(pk=animation.id).values_list('level', flat=True).first()
       print(f"level_follow: {level_follow}")
       print(f"level_animation: {level_animation}")
       if level_animation==level_follow :
           return True
       return False
   
    def search_note_of_student(self,student_id,animation_id,cycle):
        print('cycle',cycle)
        # if Note.objects.filter(student_id=student_id).exists():
        note=Note.objects.filter(student_id=student_id, animation_id=animation_id,cycle=cycle).first()
        return note
        # return None
    
    def parse_score(self, score):
        # Convertit le score en un dictionnaire
        print(f"scoreBefLoad: {score}")
        score=ast.literal_eval(score) if isinstance(score, str) else score
        for key, value in score.items(): 
            if value is None or value == 'None':
                score[key] = 0.0
            elif value < 0:
                raise serializers.ValidationError("La note ne peut pas être inférieure à 0")
            elif (value > 0 and value > 20):
                raise serializers.ValidationError("La note doit être comprise entre 0 et 20") 
            print(f"scoreAfterLoad: {score}")
            score[key]=float(value)
        return score
    
    def notify_message(self,instance, receiver, template, message_type=None):
            
        print("enter")
        print(f'instance : {instance}')
       
        student = instance.student
        print(f'student : {student}')
        print(f'receiver : {receiver}')
        # score_details = get_score_details(instance)
        
        # Préparation des données
        if instance.score is not None and isinstance(instance.score, str):
            instance.score=self.parse_score(instance.score)
            scores = [{'type': k, 'value': v} for k, v in instance.score.items()]
            print(f'scores : {scores}')
            
        scores = [instance.score]
            
        print(f'bool(scores) : {bool(scores)}')
        
        context = {
            'student_full_name': f"{student.first_name} {student.last_name}",
            'level_name': instance.animation.level.name,
            'school_name': instance.animation.school.school_name,
            'subject_name': instance.animation.subject.name,
            'current_date': format_date(date.today(), format='full', locale='fr'),
            'has_scores': bool(scores),
            'scores': scores,
            'message_type': message_type,
        }
        print(f'context : {context}')
        
        email="princedev317@gmail.com"
        email_receivers=receiver
        
        has_send=send_email_with_html_body(subject="Nouvelle note disponible", receivers=email_receivers, template=template, context=context)

        print(f"has_send : {has_send}")


    
# class NoteByStudentSerializer (serializers.ModelSerializer):
    
#     # evaluation_type= serializers.ListField(
#     #     child=serializers.CharField(),
#     #     required=False
#     # )
    
#     class Meta:
#         model=Note
#         fields=['id', 'student', 'teacher', 'academy','level', 'subject', 'coefficient', 'score', 'cycle', 'created_at', 'updated_at', 'is_validated']
        
#     def create(self, validated_data):
#         # teacher=validated_data.get('teacher')
#         # level=validated_data.get('level')
#         # subject=validated_data.get('subject')
#         # academy=validated_data.get('academy')
#         # student=validated_data.get('student')
        
        
#         # print(f"teacher : {teacher}, level : {level}, subject: {subject}, academy: {academy}")
        
#         # coefficient=self.search_coeficient(teacher=teacher)
#         # validated_data['coefficient']=coefficient
        
#         print(f"validated_data: {validated_data}")
        
        
#         try:
#             teacher_exists=self.verify_identity_teacher(teacher=teacher, level=level, subject=subject, academy=academy)
#             print(f'is_exist : {teacher_exists}')
#             if teacher_exists:
#                 search_note = self.search_note_of_student(student_id=student.id) #rechercher si la note existe déjà
#                 if search_note is not None : 
#                     note = Note.objects.create(**validated_data)
#                 else :
#                     note=self.search_note_of_student(student_id=student.id)
#                     new_score=validated_data.get('score')
#                     print(f"note: {note}")
#                     print(f"note_score: {new_score}")
#                     for key, value in new_score.items() : 
#                         print(f'key: {key}, value: {value}')
#                         note.score[key]= value
#                         note.save()
#                 return note
            
#             elif teacher_exists and self.search_note_of_student(student_id=student.id) != 'not exists':
               
#                 raise serializers.ValidationError("Les informations de l'expéditeur sont incorrectes")
    
#         except Exception as e:
#             print(f"error : {e}")
#             raise serializers.ValidationError(f"Erreur lors de l'insertion des notes, vérifier les informations saisies : {e}")
        
#     def verify_identity_teacher(teacher, level, subject, academy):
#         is_exist= Teacher.objects.filter(pk=teacher.id, level=level.pk, subject=subject.pk, academy=academy.pk).exists()
#         return is_exist
    
#     def search_coeficient(teacher):
#         teacher=Teacher.objects.filter(pk=teacher.id).first()
#         coefficient=teacher.coefficient
#         print(f"coefficient: {coefficient}")
#         return coefficient
    
#     def search_note_of_student(student_id):
#         if Note.objects.filter(student=student_id).exists():
#            note=Note.objects.filter(student=student_id).first()
#            return note
#         return None 