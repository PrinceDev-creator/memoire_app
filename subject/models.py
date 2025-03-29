from django.db import models

class Subject(models.Model):

    CATEGORY_CHOICES = [
        ('SCIENCE', 'Science'),
        ('LITERATURE', 'Litterature'),
        ('ART', 'Art'),
        ('INFORMATIQUE', 'Computer_science'),
        ('AUTRE', 'Other'),
        ('DISCIPLINE', 'Discipline')
    ]

    name= models.CharField(max_length=100)
    category=models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='category')
    
    def __str__(self):
        return self.name