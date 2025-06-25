from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Projects
from .forms import form_project
from users.models import User

class ProjectAPIViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='director@example.com',
            password='123456789',
            user_type=1,
            is_active=True
        )
        self.project = Projects.objects.create(
            title='Test Project',
            description='Initial Description',
            director=self.user
        )

    def test_delete_project(self):
        url = reverse('api-delete-project', kwargs={'pk': self.project.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Projects.objects.filter(pk=self.project.pk).exists())

    def test_edit_put_project(self):
        url = reverse('api-edit-project', kwargs={'pk': self.project.pk})
        data = {
            'title': 'Updated Project Title',
            'description': 'Fully updated description',
            'director': self.user.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Project Title')
        self.assertEqual(response.data['description'], 'Fully updated description')

    def test_edit_patch_project(self):
        url = reverse('api-edit-project', kwargs={'pk': self.project.pk})
        data = {
            'description': 'Partially updated description'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['description'], 'Partially updated description')

    def test_list_projects(self):
        url = reverse('api-list-projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_get_one_project(self):
        url = reverse('api-get-project', kwargs={'pk': self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.project.title)
        self.assertEqual(response.data['description'], self.project.description)

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