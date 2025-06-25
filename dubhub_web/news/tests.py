from django.test import TestCase
from django.urls import reverse
from users.models import User
from news.models import News, NewsMedia
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class NewsViewTests(TestCase):
    def setUp(self):
        self.news_author = User.objects.create_user('authortest@example.com', '123456789', first_name='Test Author', user_type=1, is_active=True)
        self.client.force_login(self.news_author)
        self.news = News.objects.create(title='Test News', content='This is a test news content.', author=self.news_author)
    
    def test_get_create_news(self):
        url = reverse('create-news')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_news.html')

    def test_post_create_news(self):
        url = reverse('create-news')
        data = {
            'title': 'New Test News',
            'content': 'Content for new test news.',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(News.objects.count(), 2)

        news = News.objects.get(title='New Test News')
        self.assertEqual(news.content, 'Content for new test news.')
        self.assertEqual(news.author, self.news_author)
    
    def test_delete_news(self):
        url = reverse('delete-news', args=[self.news.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(News.objects.count(), 0)
        self.assertRedirects(response, reverse('home'))

    def test_update_news(self):
        self.assertTrue(News.objects.filter(id=self.news.id).exists())
        self.assertEqual(News.objects.count(), 1)
        url = reverse('update-news', args=[self.news.id])
        data = {
            'title': 'Updated Test News',
            'content': 'Updated content for test news.',
            'author': self.news_author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_news = News.objects.get(id=self.news.id)
        self.assertEqual(updated_news.title, 'Updated Test News')
        self.assertRedirects(response, reverse('home'))

    def test_list_news(self):
        url = reverse('list-news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['news'].count(), 1)

class NewsAPIViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='author@example.com',
            password='password123',
            first_name='Author',
            is_active=True
        )
        self.client.force_login(user=self.user)
        self.news = News.objects.create(
            title='Initial News',
            content='Initial Content',
            author=self.user
        )

    def test_create_news(self):
        url = reverse('api-create-news')
        data = {
            'title': 'New News',
            'content': 'News content here',
            'author': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 2)

    def test_get_news_list(self):
        url = reverse('api-list-news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), News.objects.count())

    def test_get_news(self):
        url = reverse('api-get-news', args=[self.news.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.news.title)

    def test_update_news(self):
        url = reverse('api-update-news', args=[self.news.id])
        data = {
            'title': 'Updated News',
            'content': 'Updated Content',
            'author': self.user.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.news.refresh_from_db()
        self.assertEqual(self.news.title, 'Updated News')

    def test_delete_news(self):
        url = reverse('api-delete-news', args=[self.news.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(News.objects.filter(id=self.news.id).exists())

class NewsMediaAPIViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='author@example.com',
            password='password123',
            first_name='Author',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
        self.news = News.objects.create(
            title='News With Media',
            content='Has media attached',
            author=self.user
        )

    def test_add_news_media(self):
        url = reverse('newsmedia-list')
        file_data = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'news': self.news.id,
            'file': file_data,
            'caption': 'Image caption',
            'news_type': 1
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsMedia.objects.count(), 1)

    def test_get_news_media_list(self):
        NewsMedia.objects.create(news=self.news, file=SimpleUploadedFile("a.jpg", b"content"), news_type=0)
        url = reverse('newsmedia-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class NewsModelTests(TestCase):
    def setUp(self):
        self.news_author = User.objects.create_user('authortest@example.com', '123456789', first_name='Test Author', user_type=1, is_active=True)
        self.news = News.objects.create(title='Test News', content='This is a test news content.', author=self.news_author)
    
    def test_news_creation(self):
        news = News.objects.create(title='Another Test News', content='More test content.', author=self.news_author)
        self.assertEqual(News.objects.count(), 2)
        self.assertEqual(News.objects.get(id=news.id).title, 'Another Test News')
    
    def test_news_delete(self):
        news_id = self.news.id
        self.news.delete()
        self.assertEqual(News.objects.count(), 0)
        self.assertEqual(News.objects.filter(id=news_id).exists(), False)
    
    def test_news_update(self):
        news = News.objects.get(id=self.news.id)
        news.title = 'Updated News Title'
        news.content = 'Updated news content.'
        news.save()
        updated_news = News.objects.get(id=self.news.id)
        self.assertEqual(updated_news.title, 'Updated News Title')
        self.assertEqual(updated_news.content, 'Updated news content.')
    
    def test_news_get(self):
        news = News.objects.get(id=self.news.id)
        self.assertEqual(news.title, 'Test News')
        self.assertEqual(news.author, self.news_author)

class NewsMediaModelTest(TestCase):
    def setUp(self):
        self.news_author = User.objects.create_user('authortest@example.com', '123456789', first_name='Test Author', user_type=1, is_active=True)
        self.news = News.objects.create(title='Test News', content='Test Content', author=self.news_author)
        self.news_media = NewsMedia.objects.create(news=self.news, file='news/images/test_image.jpg', caption='Test Image Caption', news_type=0)

    def test_news_media_creation(self):
        news_media = NewsMedia.objects.create(news=self.news, file='news/images/another_image.jpg', caption='Another Image Caption', news_type=0)
        self.assertEqual(NewsMedia.objects.count(), 2)
        self.assertEqual(NewsMedia.objects.get(id=news_media.id).caption, 'Another Image Caption')
    
    def test_news_media_delete(self):
        news_media_id = self.news_media.id
        self.news_media.delete()
        self.assertEqual(NewsMedia.objects.count(), 0)
        self.assertEqual(NewsMedia.objects.filter(id=news_media_id).exists(), False)

    def test_news_media_update(self):
        news_media = NewsMedia.objects.get(id=self.news_media.id)
        news_media.file = 'news/images/updated_image.jpg'
        news_media.caption = 'Updated Image Caption'
        news_media.save()

        updated_news_media = NewsMedia.objects.get(id=self.news_media.id)
        self.assertEqual(updated_news_media.file, 'news/images/updated_image.jpg')
        self.assertEqual(updated_news_media.caption, 'Updated Image Caption')
    
    def test_news_media_get(self):
        news_media = NewsMedia.objects.get(id=self.news_media.id)
        self.assertEqual(news_media.file, 'news/images/test_image.jpg')
        self.assertEqual(news_media.caption, 'Test Image Caption')
        self.assertEqual(news_media.news, self.news)