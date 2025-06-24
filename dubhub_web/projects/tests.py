from django.test import TestCase
from django.urls import reverse

from .models import Projects
from .forms import form_project
from users.models import User

class ProjectViewTests(TestCase):
    def setUp(self):
        self.project_author = User.objects.create_user('owner@example.com', '123456789', first_name='Project Owner', is_active=True, user_type=3)
        self.client.force_login(self.project_author)
        self.project = Projects.objects.create(title='Test Project 0', description='This is a test project.', director=self.project_author)

    def test_get_create_projects(self):
        url = reverse('create-project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create.html')
        self.assertIsInstance(response.context.get('form'), form_project)

    def test_post_create_projects(self):
        data = {
            'title': 'Test Project',
            'description': 'This is a test project.',
            'director': self.project_author
        }
        url = reverse('create-project')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Projects.objects.count(), 2)
        self.assertTrue(Projects.objects.filter(title='Test Project').exists())

    def test_list_projects(self):
        url = reverse('list-projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['projects'].count(), 1)
        #self.assertEqual(len(response.context.get('projects')), 1)

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project_author = User.objects.create_user('owner@example.com', '123456789', first_name='Owner', is_active=True)
        self.project = Projects.objects.create(title='Test Project 0', description='This is a test project.', director=self.project_author)
        
    def test_project_creation(self):
        project = Projects.objects.create(
            title='Test Project',
            description='This is a test project.',
            director=self.project_author
        )
        self.assertEqual(project.title, 'Test Project')
        self.assertEqual(project.description, 'This is a test project.')
        self.assertEqual(project.director, self.project_author)
        """ self.assertTrue(project.created_at)
        self.assertTrue(project.updated_at) """
    
    def test_project_deletion(self):
        project_id = self.project.id
        Projects.objects.filter(id=project_id).delete()
        self.assertFalse(Projects.objects.filter(id=project_id).exists())

    def test_project_update(self):
        project = Projects.objects.get(id=self.project.id)
        project.title = 'Updated Test Project'
        project.description = 'This is an updated test project.'
        project.save()
        
        updated_project = Projects.objects.get(id=self.project.id)
        self.assertEqual(updated_project.title, 'Updated Test Project')
        self.assertEqual(updated_project.description, 'This is an updated test project.')
    
    def test_project_get(self):
        project = Projects.objects.get(id=self.project.id)
        self.assertEqual(project.title, 'Test Project 0')
        self.assertEqual(project.description, 'This is a test project.')
        self.assertEqual(project.director, self.project_author)