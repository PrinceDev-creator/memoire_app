from .views import FollowViewSet
from rest_framework import routers


viewsets=[
    (r'follow', FollowViewSet ,'follow'),
]

router=routers.DefaultRouter()

for route,viewset,basename in viewsets:
    router.register(route,viewset,basename=basename)
    