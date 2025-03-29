from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import SubjectSerializer
from .models import Subject

class AdminSubjectViewSet(viewsets.ModelViewSet):
    queryset=Subject.objects.all()
    # permission_classes=[IsAuthenticated,]
    serializer_class=SubjectSerializer
    
    
class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Subject.objects.all()
    # permission_classes=[IsAuthenticated,]
    serializer_class=SubjectSerializer