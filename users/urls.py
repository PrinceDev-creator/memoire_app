from rest_framework import routers
from users.views import TeacherViewSet, AcademyViewSet,TutorViewSet,UserViewSet,AdminAcademyView,AdminTeacherViewSet,AdminTutorViewSet

viewsets=[
    (r'teachers', TeacherViewSet,None),
    (r'academies', AcademyViewSet,'academies'),
    (r'tutors',TutorViewSet,None),
    (r'user/register',UserViewSet,None),
    (r'adminAcademies', AdminAcademyView,'adminAcademy'),
    (r'adminTeachers',AdminTeacherViewSet,'adminTeacher'),
    (r'adminTutors',AdminTutorViewSet, 'adminTutor')
]

router=routers.DefaultRouter()
 
for route, viewset,basename in viewsets:
    if basename :
      router.register(route,viewset,basename=basename)
    else:
        router.register(route,viewset)
