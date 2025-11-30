from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Entry

User = get_user_model()


# тест модели Entry
class EntryModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.entry = Entry.objects.create(
            user=self.user,
            title='Тестовый Заголовок',
            content='Тестовое содержимое'
        )

    def test_entry_creation(self):
        """Проверяем корректное создание Entry."""
        self.assertEqual(self.entry.title, 'Тестовый Заголовок')
        self.assertEqual(self.entry.user, self.user)
        self.assertTrue(self.entry.created_at)
        self.assertTrue(self.entry.updated_at)

    def test_entry_get_absolute_url(self):
        """Проверяет, что метод get_absolute_url возвращает правильный URL."""
        expected_url = reverse('diary:entry_detail', args=[self.entry.pk])
        self.assertEqual(self.entry.get_absolute_url(), expected_url)


# тест авторизации
class AuthenticationTests(TestCase):

    def setUp(self):
        self.list_url = reverse('diary:entry_list')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('users:register')

    def test_login_url_exists(self):
        """Проверяем, что страница входа доступна."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_register_url_exists(self):
        """Проверяем, что страница регистрации доступна."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_unauthenticated_user_redirected_on_list(self):
        """Проверяем, что неавторизованные пользователи перенаправляются."""
        response = self.client.get(self.list_url)
        # 302: Redirect
        self.assertEqual(response.status_code, 302)
        # Проверка, что перенаправление ведет на страницу входа
        self.assertTrue(response.url.startswith(self.login_url))


# тесты View Create, Update, Delete
class EntryViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Создание тестовых записей
        self.entry1 = Entry.objects.create(
            user=self.user,
            title='Заголовок для тестирования',
            content='Тестовое содержимое записи'
        )
        self.entry2 = Entry.objects.create(
            user=self.user,
            title='Другой Заголовок',
            content='Другое тестовое содержимое'
        )

        self.list_url = reverse('diary:entry_list')
        self.create_url = reverse('diary:entry_create')
        self.update_url = reverse('diary:entry_update', args=[self.entry1.pk])
        self.delete_url = reverse('diary:entry_delete', args=[self.entry1.pk])

    def test_entry_list_view_and_template(self):
        """Проверяет, что список записей доступен и использует правильный шаблон."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'diary/entry_list.html')
        # Проверяем, что обе записи пользователя отображаются
        self.assertEqual(len(response.context['entries']), 2)

    def test_entry_create_view_post_success(self):
        """Проверяет успешное создание записи через форму."""
        new_data = {'title': 'New Post', 'content': 'Content of new post'}
        response = self.client.post(self.create_url, data=new_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Entry.objects.filter(title='New Post').exists())

    def test_entry_update_view_post_success(self):
        """Проверяет успешное обновление записи через форму."""
        updated_data = {'title': 'Обновленный заголовок', 'content': 'Обновленное содержимое'}
        response = self.client.post(self.update_url, data=updated_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.entry1.refresh_from_db()
        self.assertEqual(self.entry1.title, 'Обновленный заголовок')

    def test_entry_delete_view_post_success(self):
        """Проверяет успешное удаление записи."""
        response = self.client.post(self.delete_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Entry.objects.filter(pk=self.entry1.pk).exists())

    # Тесты поиска
    def test_entry_search_by_title_or_content(self):
        """Проверяет функционал поиска по заголовку и содержимому."""

        # Поиск по заголовку
        response_title = self.client.get(self.list_url, {'q': 'тестирования'})
        self.assertEqual(len(response_title.context['entries']), 1)
        self.assertContains(response_title, self.entry1.title)

        # Поиск по содержимому
        response_content = self.client.get(self.list_url, {'q': 'Другое'})
        self.assertEqual(len(response_content.context['entries']), 1)
        self.assertContains(response_content, self.entry2.title)


# Тесты прав доступа
class EntryPermissionsTest(TestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(username='user_a', password='passwordA')
        self.user_b = User.objects.create_user(username='user_b', password='passwordB')

        self.entry_b = Entry.objects.create(
            user=self.user_b, title='User B Entry', content='Secret content of user B'
        )

        self.client.login(username='user_a', password='passwordA')  # Логинимся как UserA

        self.detail_url_b = reverse('diary:entry_detail', args=[self.entry_b.pk])
        self.update_url_b = reverse('diary:entry_update', args=[self.entry_b.pk])
        self.delete_url_b = reverse('diary:entry_delete', args=[self.entry_b.pk])
        self.list_url = reverse('diary:entry_list')

    def test_list_view_does_not_show_others_entries(self):
        """Проверяет, что UserA не видит записи UserB в своем списке."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.entry_b.title)

    def test_cannot_view_others_detail(self):
        """Проверяет, что UserA не может просмотреть чужую запись."""
        response = self.client.get(self.detail_url_b)
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

    def test_cannot_update_others_entry(self):
        """Проверяет, что UserA не может отредактировать чужую запись."""
        updated_data = {'title': 'Hacked Title', 'content': 'Hacked Content'}
        response = self.client.post(self.update_url_b, data=updated_data)

        self.assertEqual(response.status_code, 403)

    def test_cannot_delete_others_entry(self):
        """Проверяет, что UserA не может удалить чужую запись."""
        # Проверяем, что запись существует до попытки удаления
        self.assertTrue(Entry.objects.filter(pk=self.entry_b.pk).exists())

        response = self.client.post(self.delete_url_b)

        self.assertEqual(response.status_code, 403)

        # Проверяем, что запись все еще существует после неудавшейся попытки удаления
        self.assertTrue(Entry.objects.filter(pk=self.entry_b.pk).exists())
