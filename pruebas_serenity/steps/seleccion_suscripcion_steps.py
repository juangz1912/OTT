from serenity import Given, When, Then, actor
# Importa los modelos de usuario y suscripción de tu aplicación
from core.models import User, Subscription


@Given("un usuario registrado se encuentra en la página de selección de suscripción")
def abrir_pagina_seleccion_suscripcion(context):
    # Realiza la lógica para iniciar sesión en la aplicación y dirigirte a la página de selección de suscripción
    user = User.objects.create(
        username="usuarioexistente", password="contraseña")
    context.browser.get(context.base_url + "/seleccion-suscripcion")


@Given("el usuario ya tiene una suscripción Premium")
def asignar_suscripcion_premium(context):
    user = User.objects.get(username="usuarioexistente")
    Subscription.objects.create(user=user, tipo="Premium")


@When("el usuario selecciona la suscripción Gold")
def seleccionar_suscripcion_gold(context):
    context.browser.find_element_by_id("gold-subscription").click()


@Then("el usuario debe ver un mensaje de confirmación de cambio de suscripción")
def verificar_confirmacion_cambio_suscripcion(context):
    confirmation_message = context.browser.find_element_by_id(
        "confirmation-message").text
    assert "Cambio a Gold exitoso" in confirmation_message


@Then("el usuario debe tener una suscripción Gold activa")
def verificar_suscripcion_gold_activa(context):
    user = User.objects.get(username="usuarioexistente")
    subscription = Subscription.objects.get(user=user)
    assert subscription.tipo == "Gold"

# Define los pasos para otros escenarios en el mismo archivo
