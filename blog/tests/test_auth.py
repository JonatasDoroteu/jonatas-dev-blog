from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegistroTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_pagina_registro(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_registro_valido_cria_usuario(self):
        self.client.post(reverse('register'), {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
        })
        self.assertEqual(User.objects.filter(username='novousuario').count(), 1)

    def test_registro_valido_redireciona(self):
        response = self.client.post(reverse('register'), {
            'username': 'redir',
            'email': 'redir@email.com',
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
        })
        self.assertEqual(response.status_code, 302)

    def test_registro_senhas_diferentes_nao_cria(self):
        self.client.post(reverse('register'), {
            'username': 'falso',
            'email': 'falso@email.com',
            'password1': 'SenhaForte@123',
            'password2': 'SenhaDiferente@456',
        })
        self.assertEqual(User.objects.filter(username='falso').count(), 0)

    def test_registro_username_duplicado_nao_duplica(self):
        User.objects.create_user(username='existente', password='s')
        self.client.post(reverse('register'), {
            'username': 'existente',
            'email': 'x@email.com',
            'password1': 'SenhaForte@123',
            'password2': 'SenhaForte@123',
        })
        self.assertEqual(User.objects.filter(username='existente').count(), 1)


class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='loginuser', password='SenhaForte@123'
        )

    def test_get_pagina_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_correto_autentica(self):
        self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'SenhaForte@123',
        })
        response = self.client.get(reverse('home'))
        self.assertEqual(response.wsgi_request.user.username, 'loginuser')

    def test_login_correto_redireciona(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'SenhaForte@123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_senha_errada_nao_autentica(self):
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'SenhaErrada',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_usuario_inexistente_falha(self):
        response = self.client.post(reverse('login'), {
            'username': 'naoexiste',
            'password': 'qualquer',
        })
        self.assertEqual(response.status_code, 200)


class LogoutTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='sair', password='senha123')
        self.client.login(username='sair', password='senha123')

    def test_logout_desautentica(self):
        self.client.post(reverse('logout'))
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_redireciona(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)