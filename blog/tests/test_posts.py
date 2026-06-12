from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag


class CriarPostTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='criador', password='senha123'
        )
        self.client.login(username='criador', password='senha123')

    def test_get_formulario_criar(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_criar_post_valido(self):
        self.client.post(reverse('post_create'), {
            'title': 'Novo post',
            'content': 'Conteúdo do novo post',
        })
        self.assertEqual(Post.objects.filter(title='Novo post').count(), 1)

    def test_criar_post_redireciona_apos_sucesso(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'Post redirect',
            'content': 'Texto',
        })
        self.assertEqual(response.status_code, 302)

    def test_criar_post_sem_titulo_falha(self):
        self.client.post(reverse('post_create'), {
            'title': '',
            'content': 'Texto sem título',
        })
        self.assertEqual(Post.objects.filter(content='Texto sem título').count(), 0)

    def test_post_criado_pertence_ao_usuario_logado(self):
        self.client.post(reverse('post_create'), {
            'title': 'Meu post',
            'content': 'Texto',
        })
        post = Post.objects.get(title='Meu post')
        self.assertEqual(post.author, self.user)


class EditarPostTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='editor', password='senha123'
        )
        self.outro = User.objects.create_user(
            username='intruso', password='senha123'
        )
        self.post = Post.objects.create(
            title='Original', content='Texto', author=self.user
        )

    def test_autor_pode_ver_formulario_edicao(self):
        self.client.login(username='editor', password='senha123')
        url = reverse('post_update', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edicao_altera_titulo(self):
        self.client.login(username='editor', password='senha123')
        self.client.post(
            reverse('post_update', kwargs={'post_id': self.post.pk}),
            {'title': 'Título editado', 'content': 'Texto'}
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Título editado')

    def test_outro_usuario_nao_pode_editar(self):
        self.client.login(username='intruso', password='senha123')
        url = reverse('post_update', kwargs={'post_id': self.post.pk})
        response = self.client.get(url)
        self.assertIn(response.status_code, [403, 302])


class DeletarPostTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='deletador', password='senha123'
        )
        self.post = Post.objects.create(
            title='Para deletar', content='X', author=self.user
        )

    def test_deletar_remove_post(self):
        self.client.login(username='deletador', password='senha123')
        self.client.post(
            reverse('post_delete', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(Post.objects.filter(pk=self.post.pk).count(), 0)

    def test_deletar_redireciona(self):
        self.client.login(username='deletador', password='senha123')
        response = self.client.post(
            reverse('post_delete', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_anonimo_nao_pode_deletar(self):
        response = self.client.post(
            reverse('post_delete', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.filter(pk=self.post.pk).count(), 1)  