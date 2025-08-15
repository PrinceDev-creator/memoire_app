from rest_framework import routers
from users.views import TeacherViewSet, AcademyViewSet,UserViewSet,AdminAcademyViewSet,AdminTeacherViewSet,AdminUserViewSet,GenerateTeacherKeyView,CustomUserRegister

viewsets=[
    (r'teachers', TeacherViewSet,'teachers'),
    (r'academies', AcademyViewSet,'academies'),
    (r'users', AdminUserViewSet,'users'),
    # (r'tutors',TutorViewSet,'tutors'),
    # (r'user/register',UserViewSet,'usersViewSets'),
    # (r'user/customreg',CustomUserRegister,'customuserreg'),
    (r'adminAcademies', AdminAcademyViewSet,'adminAcademy'),
    (r'adminTeachers',AdminTeacherViewSet,'adminTeachers'),
    # (r'adminTutors',AdminTutorViewSet, 'adminTutors'),
    (r'generateTeacherKey',GenerateTeacherKeyView, 'generateTeacherKey')
]

router=routers.DefaultRouter()
 
for route,viewset,basename in viewsets:
  router.register(route,viewset,basename=basename)
