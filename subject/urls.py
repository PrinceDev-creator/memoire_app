from rest_framework import routers
from .views import SubjectViewSet,AdminSubjectViewSet

viewsets=[
    (r'subjects',SubjectViewSet,'subject'),
    (r'adminSubjects',AdminSubjectViewSet,'adminSubjects')
]

router=routers.DefaultRouter()
 
for route, viewset,basename in viewsets:
    if basename:
        router.register(route,viewset,basename=basename)
    else:    
        router.register(route,viewset)
    