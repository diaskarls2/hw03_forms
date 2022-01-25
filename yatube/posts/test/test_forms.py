from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from . import PostForm
from . import Post, Group

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestArt')
        cls.group = Group.objects.create(
            title='Название группы для теста',
            slug='test-slug',
            description='Описание группы для теста'
        )
        cls.post = Post.objects.create(
            text='Текст поста для теста',
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post"""
        # Посчитали количество постов
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст поста для теста',
            'group': self.group
        }
        # Отправили POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверили редирект
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'TestArt'})
        )
        # Снова проверили количество постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        # Проверили, что пост сохранился в бд
        self.assertTrue(
            Post.objects.filter(
                text='Текст поста для теста',
                group=self.group
            ).exists())

    def test_post_edit(self):
        """Валидная форма редактирует запись в Post"""
        form_data = {
            'text': 'Текст поста для теста_2',
            'post_id': '1',
            'group': self.group,
        }
        # Отправили POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': '1'}),
            data=form_data,
            follow=True,
            is_edit=True
        )
        # Проверили редирект
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': '1'})
        )
        # Проверили, что пост обновлен
        self.assertTrue(
            Post.objects.filter(
                text='Текст поста для теста_2',
                post_id='1',
                group=self.group
            ).exists())