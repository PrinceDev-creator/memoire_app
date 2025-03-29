import string,random
from faker import Faker
from level.models import Level
from subject.models import Subject
from users.models import Teacher,Academy

fake=Faker()

pair_subject_level=[]
levels=Level.objects.all()
subjects=Subject.objects.all()
academies=Academy.objects.all()

all_trio_of_academy_level_subject=[(academy,level, subject) for academy in academies for level in levels for subject in subjects]
random.shuffle(all_trio_of_academy_level_subject)


def generate_teacher_key():
        teacher_key="ens"+''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return teacher_key       

def detect_duplicate_teacher_key(teacher_key):
        while Teacher.objects.filter(teacher_key=teacher_key).exists():
                teacher_key="ens"+''.join(random.choices(string.ascii_letters + string.digits, k=10))   
        return teacher_key

def seed_teachers():

    
    for academy,level, subject in all_trio_of_academy_level_subject:
        try:
            teacher_key=generate_teacher_key()
            teacher_key=detect_duplicate_teacher_key(teacher_key)
        
            Teacher.objects.create(teacher_key=teacher_key, level=level,subject=subject, academy=academy)
        except Exception as e :
            raise Exception(e)
    
        
        
