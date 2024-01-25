from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Post, Comment


class APITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        # Создаем тестовые данные для постов и комментариев
        self.post = Post.objects.create(title='Test Post', content='Test Content', published_date='2022-01-01')
        self.comment = Comment.objects.create(post=self.post, author_name='Test Author', comment_text='Test Comment')

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_post_list_and_creation(self):
        # Проверяем, что эндпоинт для получения списка постов возвращает статус 200
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

        # Добавляем проверку создания нового поста
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, 201)  # 201 - Created

    def test_post_detail(self):
        # Проверяем, что эндпоинт для получения деталей поста возвращает статус 200
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_update(self):
        # Проверяем, что эндпоинт для обновления поста возвращает статус 200
        data = {'title': 'Updated Post', 'content': 'Updated Content'}
        response = self.client.put(f'/api/posts/{self.post.id}/', data)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что пост был действительно обновлен
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, 'Updated Post')

    def test_post_delete(self):
        # Проверяем, что эндпоинт для удаления поста возвращает статус 204 (No Content)
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 204)

        # Проверяем, что пост был действительно удален
        with self.assertRaises(Post.DoesNotExist):
            deleted_post = Post.objects.get(id=self.post.id)

    def test_comment_list_and_creation(self):
        # Проверяем, что эндпоинт для получения списка комментариев возвращает статус 200
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)

        # Добавляем проверку создания нового комментария
        data = {'post': self.post.id, 'author_name': 'New Author', 'comment_text': 'New Comment'}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, 201)  # 201 - Created

    def test_comment_detail(self):
        # Проверяем, что эндпоинт для получения деталей комментария возвращает статус 200
        response = self.client.get(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)

    def test_comment_update(self):
        # Проверяем, что эндпоинт для обновления комментария возвращает статус 200
        data = {'author_name': 'Updated Author', 'comment_text': 'Updated Comment'}
        response = self.client.put(f'/api/comments/{self.comment.id}/', data)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что комментарий был действительно обновлен
        updated_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(updated_comment.author_name, 'Updated Author')

    def test_comment_delete(self):
        # Проверяем, что эндпоинт для удаления комментария возвращает статус 204 (No Content)
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 204)

        # Проверяем, что комментарий был действительно удален
        with self.assertRaises(Comment.DoesNotExist):
            deleted_comment = Comment.objects.get(id=self.comment.id)
