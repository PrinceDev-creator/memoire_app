from urllib import request
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Level
from .serializers import LevelSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAcademyPermissions
from students.models import Student
from animation.models import Animation
from follow.models import Follow


class AdminViewSet(viewsets.ModelViewSet):
    serializer_class=LevelSerializer
    
    def get_queryset(self):
        queryset=Level.objects.all()
        school_id=self.request.GET.get('school')
        level_id=self.request.GET.get('level')
        if school_id is not None:
            queryset=Level.objects.filter(school_id=school_id)
        elif level_id is not None:
            queryset=Level.objects.filter(id=level_id)
        return queryset

class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=LevelSerializer
    
    def get_queryset(self):
        queryset=Level.objects.all()
        school_id=self.request.GET.get('school')
        if school_id is not None:
            queryset= Level.objects.filter(school_id=school_id)
        return queryset
    
class InfoLevelViewSet(APIView):
    
    def get(self, request):
        # rate={}
        level_id=request.GET.get('level')
        school_id=request.GET.get('school')
        
        if level_id is not None and school_id is not None:
            level=Level.objects.filter(pk=level_id,school_id=school_id).first()
            print(f'level : {level}')
            # students=Animation.objects.filter(level=level).values_list('students')
            
            # student_female=Student.objects.filter(level=level, sexe="F").count()
            # effective=level.effective
            
        # rate=self.gender_rate(nbr_male=student_male, nbr_female=student_female, effective=effective)
        info={
            'classname' : level.name,
            'series' : level.series,
            'group' : level.group,
            'school_name' : level.school.school_name,
            'head_teacher': level.head_teacher if level.head_teacher is not None else 'pas défini',
            'class_leader': level.class_leader if level.class_leader is not None else 'pas défini',
            # 'rate_male': rate['rate_male'],
            # 'rate_female': rate['rate_female']    
        }
        return Response(info, status=status.HTTP_200_OK)
                  
    # def gender_rate(self,nbr_male,nbr_female, effective):  
    #     # <> 
    #     no_gender=0
    #     rate={}
    #     if effective > 0 and nbr_female > 0 and nbr_male > 0 : 
    #         rate_male=(nbr_male * effective)/100
    #         rate_female=(nbr_female * effective)/100
    #     # elif nbr_male <= 0:
    #     #     rate_male=None  
    #     # elif nbr_female <= 0:
    #     #     rate_female=None
    #     rate={
    #         'rate_male' : f"{rate_male} %" if nbr_male > 0 else f"{no_gender}%" ,
    #         'rate_female' : f"{rate_female} %" if nbr_female > 0 else f"{no_gender}%"
    #     }
    #     return rate           
    # permission_classes=[IsAuthenticated,IsAcademyPermissions]
    