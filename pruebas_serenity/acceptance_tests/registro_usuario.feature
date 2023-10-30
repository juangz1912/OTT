Feature: Registro de Usuario en la aplicación

  Background: Configuración inicial
    Given un usuario no registrado se encuentra en la página de registro

  Scenario: Registro de un nuevo usuario con campos incompletos
    When el usuario intenta registrarse con campos incompletos
    Then se debe mostrar un mensaje de error indicando los campos obligatorios

  Scenario: Registro de un usuario con nombre de usuario duplicado
    And existe un usuario con el mismo nombre de usuario
    When el usuario intenta registrarse con el mismo nombre de usuario
    Then se debe mostrar un mensaje de error indicando que el nombre de usuario ya está en uso
