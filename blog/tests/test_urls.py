from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from blog.models import Post


class BlogURLsResolveTest(TestCase):
    """Testa se as URLs do blog resolvem para as views corretas."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Post de teste',
            content='Conteúdo do post de teste',
            author=self.user,
        )

    def test_home_url_resolve(self):
        url = reverse('home')
        self.assertEqual(url, '/blog/')
        resolver = resolve('/blog/')
        self.assertEqual(resolver.view_name, 'home')

    def test_post_list_url_resolve(self):
        url = reverse('post_list')
        self.assertEqual(url, '/blog/posts/')
        resolver = resolve('/blog/posts/')
        self.assertEqual(resolver.view_name, 'post_list')

    def test_post_detail_url_resolve(self):
        url = reverse('post_detail', args=[self.post.id])
        self.assertEqual(url, f'/blog/posts/{self.post.id}/')
        resolver = resolve(f'/blog/posts/{self.post.id}/')
        self.assertEqual(resolver.view_name, 'post_detail')

    def test_post_create_url_resolve(self):
        url = reverse('post_create')
        self.assertEqual(url, '/blog/posts/new/')
        resolver = resolve('/blog/posts/new/')
        self.assertEqual(resolver.view_name, 'post_create')

    def test_post_update_url_resolve(self):
        url = reverse('post_update', args=[self.post.id])
        self.assertEqual(url, f'/blog/posts/{self.post.id}/edit/')
        resolver = resolve(f'/blog/posts/{self.post.id}/edit/')
        self.assertEqual(resolver.view_name, 'post_update')

    def test_post_delete_url_resolve(self):
        url = reverse('post_delete', args=[self.post.id])
        self.assertEqual(url, f'/blog/posts/{self.post.id}/delete/')
        resolver = resolve(f'/blog/posts/{self.post.id}/delete/')
        self.assertEqual(resolver.view_name, 'post_delete')

    def test_ajax_create_category_url_resolve(self):
        url = reverse('ajax_create_category')
        self.assertEqual(url, '/blog/ajax/create-category/')
        resolver = resolve('/blog/ajax/create-category/')
        self.assertEqual(resolver.view_name, 'ajax_create_category')

    def test_ajax_create_tag_url_resolve(self):
        url = reverse('ajax_create_tag')
        self.assertEqual(url, '/blog/ajax/create-tag/')
        resolver = resolve('/blog/ajax/create-tag/')
        self.assertEqual(resolver.view_name, 'ajax_create_tag')


class BlogURLsStatusCodeTest(TestCase):
    """Testa os status HTTP das URLs do blog."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.post = Post.objects.create(
            title='Post de teste',
            content='Conteúdo do post de teste',
            author=self.user,
        )

    # ── Acesso anônimo ──────────────────────────────────────────────────────

    def test_home_anonimo_status(self):
        response = self.client.get(reverse('home'))
        self.assertIn(response.status_code, [200, 302])

    def test_post_list_anonimo_status(self):
        response = self.client.get(reverse('post_list'))
        self.assertIn(response.status_code, [200, 302])

    def test_post_create_anonimo_redireciona(self):
        """Usuário anônimo deve ser redirecionado ao tentar criar post."""
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)

    def test_post_update_anonimo_redireciona(self):
        response = self.client.get(reverse('post_update', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)

    def test_post_delete_anonimo_redireciona(self):
        response = self.client.get(reverse('post_delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)

    # ── Acesso autenticado ──────────────────────────────────────────────────

    def test_home_autenticado_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertIn(response.status_code, [200, 302])

    def test_post_list_autenticado_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_list'))
        self.assertIn(response.status_code, [200, 302])

    def test_post_create_autenticado_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_create'))
        self.assertIn(response.status_code, [200, 302])

    def test_post_detail_autenticado_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertIn(response.status_code, [200, 302])

    def test_post_update_autenticado_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_update', args=[self.post.id]))
        self.assertIn(response.status_code, [200, 302])

    def test_post_delete_autenticado_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('post_delete', args=[self.post.id]))
        self.assertIn(response.status_code, [200, 302])

    # ── AJAX endpoints ──────────────────────────────────────────────────────

    def test_ajax_create_category_requer_post(self):
        """Endpoint AJAX deve rejeitar GET ou exigir autenticação."""
        response = self.client.get(reverse('ajax_create_category'))
        self.assertIn(response.status_code, [302, 403, 405])

    def test_ajax_create_tag_requer_post(self):
        response = self.client.get(reverse('ajax_create_tag'))
        self.assertIn(response.status_code, [302, 403, 405])


class ConfigURLsResolveTest(TestCase):
    """Testa se as URLs do config (raiz do projeto) resolvem corretamente."""

    def test_root_redireciona_para_blog(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/blog/', response['Location'])

    def test_admin_url_resolve(self):
        resolver = resolve('/admin/')
        self.assertEqual(resolver.app_name, 'admin')

    def test_login_url_resolve(self):
        url = reverse('login')
        resolver = resolve(url)
        self.assertIsNotNone(resolver)

    def test_logout_url_resolve(self):
        url = reverse('logout')
        resolver = resolve(url)
        self.assertIsNotNone(resolver)

    def test_accounts_login_url_resolve(self):
        url = reverse('accounts_login')
        resolver = resolve(url)
        self.assertIsNotNone(resolver)

    def test_api_token_url_resolve(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(url, '/api/token/')

    def test_api_token_refresh_url_resolve(self):
        url = reverse('token_refresh')
        self.assertEqual(url, '/api/token/refresh/')

    def test_api_schema_url_resolve(self):
        url = reverse('schema')
        self.assertEqual(url, '/api/schema/')

    def test_api_docs_url_resolve(self):
        url = reverse('swagger-ui')
        self.assertEqual(url, '/api/docs/')

    def test_sitemap_url_resolve(self):
        url = reverse('sitemap')
        self.assertEqual(url, '/sitemap.xml')


class ConfigURLsStatusCodeTest(TestCase):
    """Testa os status HTTP das URLs raiz do projeto."""

    def setUp(self):
        self.client = Client()

    def test_root_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_page_status(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_sitemap_status(self):
        response = self.client.get('/sitemap.xml')
        self.assertIn(response.status_code, [200, 404])

    def test_api_schema_status(self):
        response = self.client.get('/api/schema/')
        self.assertIn(response.status_code, [200, 301, 302])

    def test_api_docs_status(self):
        response = self.client.get('/api/docs/')
        self.assertIn(response.status_code, [200, 301, 302])