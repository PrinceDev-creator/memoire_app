from rest_framework import routers
from .views import LevelViewSet,AdminViewSet

viewsets=[
    (r'levels', LevelViewSet,'level'),
    (r'adminLevels', AdminViewSet,'adminLevel')
]

router=routers.DefaultRouter()
 
for route, viewset,basename in viewsets:
    if basename:
        router.register(route,viewset,basename=basename)
    else:    
        router.register(route,viewset)
    