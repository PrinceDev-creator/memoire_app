from .views import SchoolViewSet
from rest_framework import routers

router=routers.DefaultRouter()

viewsets=[
    (r'schools',SchoolViewSet, 'schools')
]

for route,viewset,basename in viewsets:
    router.register(route,viewset,basename=basename)