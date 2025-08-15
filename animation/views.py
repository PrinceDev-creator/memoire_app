import random
import string
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Animation
from .serializers import AddLevelSubjectSerializer, AssociateTeacherToAnimationKeySerializer, AnimationSerializer

class AddLevelSubjectViewSet(APIView):
    
    def post(self,request, *args, **kwargs):
        
        data=request.data.copy()
        
        print(f'data : {data}')
        
        serializer=AddLevelSubjectSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save()
        return Response({'message': 'Association matière-classe créée avec succès'},status=201)
        
    
class AssociateTeacherToAnimationKeyViewSet(APIView):    
        
        
    def patch(self, request, *args, **kwargs):
        animation_key=request.data.get('animation_key')
        animation_key=str(animation_key).strip()
        if not animation_key:  
            return Response({'error': 'Clé d\'animation manquante'}, status=400)
        
        print(f'animation_key : {animation_key}')
        
        try:
            animation=self.search_animation(animation_key)
            print(f"animation : {animation}")
            if animation.teacher!=None :
                return Response({'error': ' Clé non valide : Un enseignant est rattaché à cette clé'}, status=500)
            elif animation==None:
                return Response({'error': ' Clé non valide : Cette clé n\'existe pas'}, status=500)    
                
            print(f"animation : {animation}")
            serializer=AssociateTeacherToAnimationKeySerializer(instance=animation, data=request.data, partial=True)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            
            serializer.save()
            return Response(serializer.data, status=200)
            
        except Exception as e:
            raise ValidationError(f'Une erreur s\'est produite {e}' )
        
    def search_animation(self, animation_key):
        animation=Animation.objects.filter(animation_key=animation_key).first()
        return animation 
        
class AnimationViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class=AnimationSerializer
    queryset=Animation.objects.all()
    
    
def animation_list(request):
    animations=Animation.objects.all()
    return render(request,'animations/list_animations.html', {'animations': animations})