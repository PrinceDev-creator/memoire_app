from rest_framework import viewsets
from .models import Level
from .serializers import LevelSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAcademyPermissions



class AdminViewSet(viewsets.ModelViewSet):
    queryset=Level.objects.all()
    serializer_class=LevelSerializer

class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Level.objects.all()
    serializer_class=LevelSerializer
    # permission_classes=[IsAuthenticated,IsAcademyPermissions]
    