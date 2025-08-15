from .views import ProfilTutorViewSet
from rest_framework import routers

router=routers.DefaultRouter()

viewsets=[
    (r'tutors',ProfilTutorViewSet, 'tutors')
]

for route,viewset,basename in viewsets:
    router.register(route,viewset,basename=basename)