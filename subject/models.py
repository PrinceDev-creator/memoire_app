from django.db import models

class Subject(models.Model):

    # CATEGORY_CHOICES = [
    #     ('SCIENCE', 'Science'),
    #     ('LITERATURE', 'Littérature'),
    #     ('ART', 'Art'),
    #     ('COMPUTER_SCIENCE', 'Informatique'),
    #     ('OTHER', 'Autre'),
    #     ('DISCIPLINE', 'Discipline')
    # ]

    name= models.CharField(max_length=100)
    category=models.CharField(max_length=50, default='category')
    school=models.ForeignKey('school.School', on_delete=models.CASCADE, default=1, null=True)
    pseudo=models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name