from rest_framework import routers
from .views import AnimationViewset

viewsets=[
    (r'animations', AnimationViewset, 'animation'),
]

router=routers.DefaultRouter()

for route,viewset,basename in viewsets :
    router.register(route,viewset,basename=basename)