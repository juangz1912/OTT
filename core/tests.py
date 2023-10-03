from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ValidationError

class LoginViewTestCase(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page_loads_properly(self):
        # Prueba que la página de inicio de sesión cargue correctamente
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/registration/login.html')  # Ajusta la ruta de la plantilla aquí

    def test_login_form(self):
        # Prueba que el formulario de inicio de sesión esté presente en la página
        response = self.client.get(reverse('login'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'type="submit"')

    def test_successful_login(self):
        # Prueba el inicio de sesión exitoso
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Debería redirigir después de un inicio de sesión exitoso

    def test_failed_login(self):
        # Prueba el inicio de sesión fallido con credenciales incorrectas
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'incorrectpassword'})
        self.assertEqual(response.status_code, 200)  # Debería volver a la página de inicio de sesión
        self.assertFormError(response, 'form', None, 'Por favor, introduzca un nombre de usuario y contraseña válidos.')

    def test_non_field_errors(self):
        # Prueba que los errores no relacionados con campos se muestren correctamente
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'incorrectpassword'})
        self.assertContains(response, 'Por favor, introduzca un nombre de usuario y contraseña válidos.')

    def test_csrf_token(self):
        # Prueba que el token CSRF esté presente en el formulario
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_links(self):
        # Prueba que los enlaces a las páginas de inicio y registro estén presentes
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('register'))

# Create your tests here.
