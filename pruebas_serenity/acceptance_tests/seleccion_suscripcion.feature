Feature: Selección de Suscripciones en la aplicación

  Background: Configuración inicial
    Given un usuario registrado se encuentra en la página de selección de suscripción

  Scenario: Cambio de suscripción de un usuario existente a Gold
    And el usuario ya tiene una suscripción Premium
    When el usuario selecciona la suscripción Gold
    Then el usuario debe ver un mensaje de confirmación de cambio de suscripción
    And el usuario debe tener una suscripción Gold activa

  Scenario: Cambio de suscripción de un usuario existente a Premium
    And el usuario ya tiene una suscripción Gold
    When el usuario selecciona la suscripción Premium
    Then el usuario debe ver un mensaje de confirmación de cambio de suscripción
    And el usuario debe tener una suscripción Premium activa
