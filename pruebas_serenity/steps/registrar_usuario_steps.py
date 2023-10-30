from serenity import Given, When, Then, actor
from selenium.webdriver.common.keys import Keys
from core.models import User  # Importa el modelo de usuario de tu aplicación


@Given("un usuario no registrado se encuentra en la página de registro")
def abrir_pagina_registro(context):
    context.browser.get(context.base_url + "/registro")


@When("el usuario intenta registrarse con campos incompletos")
def registrar_usuario_campos_incompletos(context):
    context.browser.find_element_by_id("id_username").send_keys("")


@Then("se debe mostrar un mensaje de error indicando los campos obligatorios")
def verificar_mensaje_campos_incompletos(context):
    error_message = context.browser.find_element_by_id("error-message").text
    assert "Campos obligatorios" in error_message


@Given("un usuario no registrado se encuentra en la página de registro")
def abrir_pagina_registro(context):
    context.browser.get(context.base_url + "/registro")


@Given("existe un usuario con el mismo nombre de usuario")
def crear_usuario_existente(context):
    User.objects.create(username="usuarioexistente", password="contraseña")


@When("el usuario intenta registrarse con el mismo nombre de usuario")
def registrar_usuario_duplicado(context):
    context.browser.find_element_by_id(
        "id_username").send_keys("usuarioexistente")


@Then("se debe mostrar un mensaje de error indicando que el nombre de usuario ya está en uso")
def verificar_mensaje_usuario_duplicado(context):
    error_message = context.browser.find_element_by_id("error-message").text
    assert "Nombre de usuario en uso" in error_message
