from .views import ProfilTeacherViewSet
from rest_framework import routers

router=routers.DefaultRouter()

viewsets=[
    (r'teachers',ProfilTeacherViewSet, 'teachers')
]

for route,viewset,basename in viewsets:
    router.register(route,viewset,basename=basename)