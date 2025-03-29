from rest_framework import routers
from .views import StudentViewSet,AdminStudentViewSet

viewsets=[
    (r'students',StudentViewSet,'student'),
    (r'adminStudents',AdminStudentViewSet,'adminStudent')
]

router=routers.DefaultRouter()
 
for route, viewset,basename in viewsets:
    if basename:
        router.register(route,viewset,basename=basename)
    else:    
        router.register(route,viewset)
    