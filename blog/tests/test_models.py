from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='senha123'
        )

    def test_criacao_usuario(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_str_usuario(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_usuario_autenticavel(self):
        self.assertTrue(self.user.check_password('senha123'))

    def test_usuario_nao_admin_por_padrao(self):
        self.assertFalse(self.user.is_staff)


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Tecnologia',
            slug='tecnologia'
        )

    def test_criacao_categoria(self):
        self.assertEqual(self.category.name, 'Tecnologia')
        self.assertEqual(self.category.slug, 'tecnologia')

    def test_str_categoria(self):
        self.assertEqual(str(self.category), 'Tecnologia')


class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(
            name='Python',
            slug='python'
        )

    def test_criacao_tag(self):
        self.assertEqual(self.tag.name, 'Python')
        self.assertEqual(self.tag.slug, 'python')

    def test_str_tag(self):
        self.assertEqual(str(self.tag), 'Python')


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='autor', password='senha123'
        )
        self.category = Category.objects.create(
            name='Django', slug='django'
        )
        self.tag = Tag.objects.create(
            name='Web', slug='web'
        )
        self.post = Post.objects.create(
            title='Post de teste',
            content='Conteúdo do post',
            author=self.user,
            category=self.category
        )
        self.post.tags.add(self.tag)

    def test_criacao_post(self):
        self.assertEqual(self.post.title, 'Post de teste')
        self.assertEqual(self.post.author, self.user)

    def test_str_post(self):
        self.assertEqual(str(self.post), 'Post de teste')

    def test_post_tem_categoria(self):
        self.assertEqual(self.post.category, self.category)

    def test_post_tem_tag(self):
        self.assertIn(self.tag, self.post.tags.all())

    def test_post_sem_categoria_permitido(self):
        post = Post.objects.create(
            title='Sem categoria',
            content='Texto',
            author=self.user
        )
        self.assertIsNone(post.category)

    def test_post_pertence_ao_usuario(self):
        posts_do_user = Post.objects.filter(author=self.user)
        self.assertIn(self.post, posts_do_user)

    def test_datas_preenchidas_automaticamente(self):
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)