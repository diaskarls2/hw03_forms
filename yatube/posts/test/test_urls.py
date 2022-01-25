from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Название группы для теста',
            slug='test-slug',
            description='Описание группы для теста'
        )
        cls.post = Post.objects.create(
            text='Текст поста для теста',
            pk=15
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Test_Dias')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_homepage(self):
        """Страница index доступна любому пользователю."""
        response = self.guest_client.get('')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_grouppage(self):
        """Страница group_list доступна любому пользователю."""
        response = self.guest_client.get('/group/<slug>/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_profilepage(self):
        """Страница profile доступна любому пользователю."""
        response = self.guest_client.get('profile/<username>/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_post_detailpage(self):
        """Страница post_detail доступна любому пользователю."""
        response = self.guest_client.get('posts/<post_id>/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_unexistingpage(self):
        """Страница не существует."""
        response = self.guest_client.get()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_createpage(self):
        """Страница create доступна авторизованному пользователю."""
        response = self.authorized_client.get('create/')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_post_editpage(self):
        """Страница post_edit доступна автору поста."""
        response = self.authorized_client.force_login(self.user)(
            'posts/<post_id>/edit')
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_urls_posts_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/<slug>/': 'posts/group_list.html',
            'profile/<username>/': 'posts/profile.html',
            'posts/<post_id>/': 'posts/post_detail.html',
            'posts/<post_id>/edit': 'posts/create_post.html',
            'create/': 'posts/create_post.html',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template, 'Шаблон не найден')