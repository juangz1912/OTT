from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import Item, Item2, Item3, Item4

class LoginViewTestCase(TestCase):
    def setUp(self):
        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_page_loads_properly(self):
        # Prueba que la página de inicio de sesión cargue correctamente
        response = self.client.get(reverse('login')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/registration/login.html')

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
        self.assertEqual(response.status_code, 302) 

    def test_failed_login(self):
        # Prueba el inicio de sesión fallido con credenciales incorrectas
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'incorrectpassword'})
        self.assertEqual(response.status_code, 200)
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

