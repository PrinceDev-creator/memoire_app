from django.core.validators import MinValueValidator, MaxValueValidator
from subject.models import Subject
from django.apps import apps
from students.models import Student


Subject=apps.get_model('subject','Subject')