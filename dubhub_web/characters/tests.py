from django.test import TestCase
from django.urls import reverse

from characters.models import Character
from users.models import User

class CharacterViewTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser@example.com', '123456789')
        self.client.force_login(self.test_user)
        self.character = Character.objects.create(name='Test character', description='THis is a test character', voice_type=0, gender=0)
    
    def test_get_create_character(self):
        url = reverse('create-character')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_character.html')
    
    def test_post_create_character(self):
        url = reverse('create-character')
        data = {
            'name': 'Test Character',
            'description': 'This is a test character.',
            'gender' : 0,
            'voice_type': 0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('list-characters'))
        self.assertEqual(Character.objects.count(), 2)
    
    def test_list_characters(self):
        url = reverse('list-characters')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_character(self):
        url = reverse('delete-character', args=self.test_user.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 204)


class CharactersModelTests(TestCase):
    def setUp(self):
        self.character = Character.objects.create(name='Test Character', gender=0, description='This is a test character.')
    
    def test_character_creation(self):
        character = Character.objects.create(name='New Test Character', gender=0, description='This is a new test character.')
        self.assertEqual(Character.objects.count(), 2)
        self.assertTrue(Character.objects.filter(name='New Test Character').exists())
        self.assertEqual(Character.objects.get(name='New Test Character').description, 'This is a new test character.')
    
    def test_character_delete(self):
        character_id = self.character.id
        self.character.delete()
        self.assertEqual(Character.objects.count(), 0)
        self.assertFalse(Character.objects.filter(id=character_id).exists())
    
    def test_character_update(self):
        self.character.name = 'Updated Test Character'
        self.character.description = 'Updated description for test character.'
        self.character.save()
        updated_character = Character.objects.get(id=self.character.id)
        self.assertEqual(updated_character.name, 'Updated Test Character')
        self.assertEqual(updated_character.description, 'Updated description for test character.')