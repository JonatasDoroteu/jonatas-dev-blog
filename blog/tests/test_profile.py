from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class VisualizarPerfilTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='perfil_user',
            email='perfil@email.com',
            password='senha123'
        )

    def test_ver_perfil_logado(self):
        self.client.login(username='perfil_user', password='senha123')
        response = self.client.get(reverse('profile'))  # ← ajuste abaixo
        self.assertEqual(response.status_code, 200)

    def test_perfil_exibe_username(self):
        self.client.login(username='perfil_user', password='senha123')
        response = self.client.get(reverse('profile'))
        self.assertContains(response, 'perfil_user')

    def test_anonimo_redireciona_do_perfil(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)


class EditarPerfilTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='edit_profile',
            email='old@email.com',
            password='senha123'
        )
        self.client.login(username='edit_profile', password='senha123')

    def test_get_formulario_edicao(self):
        response = self.client.get(reverse('profile_edit'))  # ← ajuste abaixo
        self.assertEqual(response.status_code, 200)

    def test_editar_email(self):
        self.client.post(reverse('profile_edit'), {
            'username': 'edit_profile',
            'email': 'novo@email.com',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'novo@email.com')

    def test_edicao_redireciona(self):
        response = self.client.post(reverse('profile_edit'), {
            'username': 'edit_profile',
            'email': 'r@email.com',
        })
        self.assertEqual(response.status_code, 302)

    def test_anonimo_nao_acessa_edicao(self):
        self.client.logout()
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 302)