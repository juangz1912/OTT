from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import Item, Item2, Item3, Item4
from unittest.mock import MagicMock, patch


class LoginViewTestCase(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_login_page_loads_properly(self):
        # Prueba que la página de inicio de sesión cargue correctamente
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'core/templates/registration/login.html')

    def test_login_form(self):
        # Prueba que el formulario de inicio de sesión esté presente en la página
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'type="submit"')

    def test_successful_login(self):
        # Prueba el inicio de sesión exitoso
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def test_failed_login(self):
        # Prueba el inicio de sesión fallido con credenciales incorrectas
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'incorrectpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', None, 'Por favor, introduzca un nombre de usuario y contraseña válidos.')

    def test_non_field_errors(self):
        # Prueba que los errores no relacionados con campos se muestren correctamente
        response = self.client.post(
            reverse('login'), {'username': 'testuser', 'password': 'incorrectpassword'})
        self.assertContains(
            response, 'Por favor, introduzca un nombre de usuario y contraseña válidos.')

    def test_csrf_token(self):
        # Prueba que el token CSRF esté presente en el formulario
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_links(self):
        # Prueba que los enlaces a las páginas de inicio y registro estén presentes
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('register'))


class RegisterViewTestCase(TestCase):
    def test_register_page_loads_properly(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        # Ajusta la ruta de la plantilla aquí
        self.assertTemplateUsed(
            response, 'core/templates/registration/register.html')

    def test_register_form(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')
        self.assertContains(response, 'type="submit"')

    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('register'), data)
        # Debería redirigir después de un registro exitoso
        self.assertEqual(response.status_code, 302)

    def test_failed_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'differentpassword',  # Contraseña diferente
        }
        response = self.client.post(reverse('register'), data)
        # Debería volver a la página de registro
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2',
                             'Las contraseñas no coinciden.')

    def test_user_created(self):
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.client.post(reverse('register'), data)
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)

    def test_logged_in_after_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(self.client.session['_auth_user_id'], str(
            User.objects.get(username='testuser').id))

    def test_redirect_after_successful_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(reverse('register'), data, follow=True)
        # Verifica que redirija a la página de inicio o a donde corresponda
        self.assertEqual(response.status_code, 200)


class ProductViewTestCase(TestCase):
    def setUp(self):
        # Crea algunos objetos de modelo de ejemplo para usar en las pruebas
        Item.objects.create(video='<URL_DEL_VIDEO_Item>')
        Item2.objects.create(video='<URL_DEL_VIDEO_Item2>')
        Item3.objects.create(video='<URL_DEL_VIDEO_Item3>')
        Item4.objects.create(video='<URL_DEL_VIDEO_Item4>')
        # Crea más objetos según sea necesario

    def test_product_page_loads_properly(self):
        # Prueba que la página de productos cargue correctamente
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/core/products.html')

#
#
# PRUEBAS CON MOCK
#
#


class LoginViewTestCaseMock(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_successful_login(self):
        # Prueba el inicio de sesión exitoso
        with patch('django.contrib.auth.authenticate') as mock_authenticate:
            # Configura el mock para que devuelva el usuario de prueba
            mock_authenticate.return_value = self.user
            response = self.client.post(
                reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        self.assertEqual(response.status_code, 302)

    def test_failed_login(self):
        # Prueba el inicio de sesión fallido con credenciales incorrectas
        with patch('django.contrib.auth.authenticate') as mock_authenticate:
            # Configura el mock para que devuelva None, simulando un inicio de sesión fallido
            mock_authenticate.return_value = None
            response = self.client.post(
                reverse('login'), {'username': 'testuser', 'password': 'incorrectpassword'})

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 'form', None, 'Por favor, introduzca un nombre de usuario y contraseña válidos.')


class RegisterViewTestCaseMock(TestCase):
    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        # Simula el envío del formulario de registro
        with patch('django.contrib.auth.models.User.objects.create_user'):
            response = self.client.post(reverse('register'), data)

        # Debería redirigir después de un registro exitoso
        self.assertEqual(response.status_code, 302)
