"""
URL configuration for edutrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
import os

# Ajoutez le répertoire racine du projet dans PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.urls import router as users_routers
from subject.urls import router as subjects_routers
from note.urls import router as notes_routers
from level.urls import router as levels_routers
from students.urls import router as students_routers
from animation.urls import router as animations_routers
from follow.urls import router as follows_routers
from school.urls import router as schools_routers
from teacher.urls import router as teachers_routers
from tutor.urls import router as tutors_routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from rest_framework.authtoken.views import obtain_auth_token
from users.views import DefPassword, TestView,CustomLoginView, run_auto_seed_teachers,CustomUserRegister
from note.views import StudentStatisticsView,SendReportCardAPIView,StudentAverageView, EditNoteViewSet
from students.views import SchoolStudentsView, StudentFollowCreateView,LevelStudentsView, student_list
from animation.views import AddLevelSubjectViewSet, AssociateTeacherToAnimationKeyViewSet, animation_list
from pre_registration.views import PreRegistrationView,print_hello,school_list_view,reject_registration_view
from level.views import InfoLevelViewSet
from subject.views import SubjectsLevelView, SubjectsSchoolView
from school.views import reportTest, view_school_notes
from follow.views import AssignLevelToFollowView,AssociateTutorToStudentView,follow_list
from teacher.views import teacher_list
from tutor.views import tutor_list
from school.views import school_list
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="EduTrack API",
      default_version='v1',
      description="Documentation de l'API EduTrack",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@princedev.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


routers_elements=[
    (users_routers),
    (subjects_routers),
    (notes_routers),
    (levels_routers),
    (students_routers),
    (animations_routers),
    (follows_routers),
    (teachers_routers),
    (tutors_routers),
    (schools_routers)
]

router = routers.DefaultRouter()
for router_element in routers_elements:
    router.registry.extend(router_element.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_access'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', TestView.as_view(), name='testView'),
    path('auth/', include('dj_rest_auth.urls')),
    # path('auth/signup/',CustomRegisterView.as_view(),name="custom_register"),
    path('auth/registration/',include('dj_rest_auth.registration.urls')),
    path('api-token-auth/',obtain_auth_token,name='api_token_auth'),  
    path('user/login/', CustomLoginView.as_view(), name='login'),
    path('statistics/', StudentStatisticsView.as_view(),name='statistics'),
    path('student-average/', StudentAverageView.as_view(), name='student-average'),
    path('edit-note/', EditNoteViewSet.as_view(), name='edit-note'),
    path('generate-teacher-key/',run_auto_seed_teachers,name='generate-teacher-key'),
    path('user/register/', CustomUserRegister.as_view(),name='custom-register'),
    path('user/defpassword/', DefPassword.as_view(),name='definy-password'),
    path('animation_list/', animation_list, name='animation-list'),
    path('animate-level/',AddLevelSubjectViewSet.as_view(),name='animate'),
    path("animate-teacher/", AssociateTeacherToAnimationKeyViewSet.as_view(), name="associateTeacher"),
    path("associate-tutor/", AssociateTutorToStudentView.as_view(), name="associateStudent"),
    path('pre-registration/',PreRegistrationView.as_view(), name='pre_registration'),
    path('print-hello/',print_hello, name='print_hello'),
    path('schools-preg/', school_list_view, name='school_list_preg'),
    path('reject_registration/', reject_registration_view, name='reject_registration'),
    path('level-info/', InfoLevelViewSet.as_view(), name='infos_level'),
    path('level-students/',LevelStudentsView.as_view(), name='level_students'),
    path('school-students/', SchoolStudentsView.as_view(), name='school_students'),
    path('level-subjects/',SubjectsLevelView.as_view(), name='level-subjects'),
    path('school-subjects/', SubjectsSchoolView.as_view(), name='school-subjects'),
    path('school_list/', school_list, name='school-list'),
    path('teacher_list/',teacher_list, name='teacher-list'),
    path('tutor_list/', tutor_list, name='tutor-list'),
    path('student_list/', student_list, name='student-list'),
    path('follow_list/',follow_list, name='follow-list'),
    path('report/', reportTest, name='reportTest'),
    path('send-report-card/', SendReportCardAPIView.as_view(), name='send-report-card'),
    path('create-student-follow/', StudentFollowCreateView.as_view(), name='create-student-follow'),
    path('assign-level/', AssignLevelToFollowView.as_view(), name='assign-level-to-follow'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('view-school-notes/', view_school_notes, name='view-school-notes'),
]
