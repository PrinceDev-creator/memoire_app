import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from school.models import School
from teacher.models import Teacher
from students.models import Student
from level.models import Level


nbr_level=input("Entrer le nombre de classe que vous désirer créer: ")
while True:
    try:
        nbr_level=int(nbr_level)
        if nbr_level > 0 : 
            break
        else : 
            print("Veuillez entrer un nombre supérieur à 0")
    except ValueError:
        print("Veuiller entrer un entier supérieur à 0")
nbr_level=int(nbr_level)

class Command(BaseCommand):
    help = 'Seed the Level model with sample data'

    level_name=''

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        # Récupérer les écoles, enseignants et étudiants existants
        schools = School.objects.all()
        # teachers = Teacher.objects.all()
        # students = Student.objects.all()


        if not schools.exists():
            self.stdout.write(self.style.ERROR('Aucune école trouvée. Veuillez créer des écoles d\'abord.'))
            return


        for _ in range(nbr_level):
            name = self.choice_level_name()
            group = self.choice_group()
            series = self.choice_series()
            school = random.choice(schools)
            
            # Vérifie si la combinaison existe déjà
            if not Level.objects.filter(
                name=name,
                group=group,
                series=series,
                school=school
            ).exists():
                Level.objects.create(
                    name=name,
                    group=group,
                    series=series,
                    school=school,
                    effective=random.randint(10, 50),
                )

        # inserted_pks = seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {nbr_level} Level instances'))


    def choice_level_name(self):
        self.level_name = random.choice([
            "6eme", "5eme", "4eme", "3eme",
            "2nde", "1ere", "Terminale",
        ])

        return self.level_name


    def choice_group(self):
        groups = ["A", "B", "C", "D","1", "2","3" ,None]

        if self.level_name in ["6eme", "5eme", "4eme", "3eme"]:
            groups = ["A", "B", "C", "D"]
        elif self.level_name in ["2nde", "1ere", "Terminale"]:
            groups = ["1", "2", "3",None]

        return random.choice(groups)


    def choice_series(self):
        series = ["S", "A", "B", "C", "D", "G2", "F4", None]

        if self.level_name in ["6eme", "5eme", "4eme", "3eme"]:
            series = [None]
        elif self.level_name in ["2nde", "1ere", "Terminale"]:
            series = ["S", "A", "B", "C", "D"]

        return random.choice(series)

    # def choice_effective(self):
    #     return random.randint(10, 50)
