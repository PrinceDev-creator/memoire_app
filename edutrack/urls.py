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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from rest_framework.authtoken.views import obtain_auth_token
from users.views import TestView,CustomLoginView, run_auto_seed_teachers
from note.views import StudentStatisticsView

routers_elements=[
    (users_routers),
    (subjects_routers),
    (notes_routers),
    (levels_routers),
    (students_routers)
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
    path('generate-teacher-key/',run_auto_seed_teachers,name='generate-teacher-key')
]
