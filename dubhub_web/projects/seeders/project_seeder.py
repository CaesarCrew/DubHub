from jessilver_django_seed.seeders.BaseSeeder import BaseSeeder
from projects.models import Projects
from users.models import User

class ProjectsSeeder(BaseSeeder):
    @property
    def seeder_name(self):
        return 'ProjectsSeeder'

    def seed(self):
        if not Projects.objects.count() > 0:
            director = User.objects.filter(user_type=4).first()
            Projects.objects.create(title='Default Title', description='Default project description', director=director)
            self.success(f'Project created')
        else:
            self.error(f'Project already exists')