from django.urls import path
from rest_framework import routers
from .views import NoteViewSet,AdminNotesViewSet,StudentStatisticsView

viewsets=[
    (r'notes',NoteViewSet,'note'),
    (r'adminNotes', AdminNotesViewSet,'adminNotes'),
]

router=routers.DefaultRouter()
 
for route,viewset,basename in viewsets:
    if basename:
        router.register(route,viewset,basename=basename)
    else:    
        router.register(route,viewset)
     
   
        
# <int:student>/<int:level>/<int:cycle>/<int:subject>        
        