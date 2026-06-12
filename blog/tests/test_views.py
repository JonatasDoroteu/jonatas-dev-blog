from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewer', password='senha123'
        )

    def test_home_retorna_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_contem_posts(self):
        Post.objects.create(
            title='Post visível',
            content='Texto',
            author=self.user
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Post visível')


class PostListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='listador', password='senha123'
        )
        Post.objects.create(title='Post A', content='C', author=self.user)
        Post.objects.create(title='Post B', content='C', author=self.user)

    def test_lista_retorna_200(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_lista_exibe_posts(self):
        response = self.client.get(reverse('post_list'))
        self.assertContains(response, 'Post A')
        self.assertContains(response, 'Post B')


class PostDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='leitor', password='senha123'
        )
        self.post = Post.objects.create(
            title='Detalhe do post',
            content='Conteúdo detalhado',
            author=self.user
        )

    def test_detalhe_retorna_200(self):
        url = reverse('post_detail', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detalhe_exibe_titulo(self):
        url = reverse('post_detail', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertContains(response, 'Detalhe do post')

    def test_post_inexistente_retorna_404(self):
        url = reverse('post_detail', kwargs={'post_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ViewsProtegidасTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_criar_post_redireciona_anonimo(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)

    def test_editar_post_redireciona_anonimo(self):
        user = User.objects.create_user(username='ed', password='s')
        post = Post.objects.create(title='T', content='C', author=user)
        response = self.client.get(
            reverse('post_update', kwargs={'post_id': post.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_deletar_post_redireciona_anonimo(self):
        user = User.objects.create_user(username='ed2', password='s')
        post = Post.objects.create(title='T2', content='C', author=user)
        response = self.client.post(
            reverse('post_delete', kwargs={'post_id': post.pk})
        )
        self.assertEqual(response.status_code, 302)