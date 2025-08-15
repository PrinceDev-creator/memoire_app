from django.urls import path
from rest_framework import routers
from .views import NoteViewSet,AdminNotesViewSet,StudentStatisticsView, AddNoteViewSet

viewsets=[
    (r'notes',NoteViewSet,'notes'),
    (r'adminNotes', AdminNotesViewSet,'adminNotes'),
    (r'addNotes', AddNoteViewSet,'addNotes')
    
]

router=routers.DefaultRouter()
 
for route,viewset,basename in viewsets:
    if basename:
        router.register(route,viewset,basename=basename)
    else:    
        router.register(route,viewset)
     
   
        
# <int:student>/<int:level>/<int:cycle>/<int:subject>        
        