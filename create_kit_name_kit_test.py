# create_kit_name_kit_test.py

import copy
import pytest
import data
import sender_stand_request

# Genera un body personalizado con el nombre que se desee
def get_kit_body(name):
    body = copy.deepcopy(data.kit_body)
    body["name"] = name
    return body

# Verificación positiva
def positive_assert(kit_body):
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(kit_body, token)
    assert response.status_code in (200, 201)
    assert response.json()["name"] == kit_body["name"]

# Verificación negativa para errores 400
def negative_assert_code_400(kit_body):
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(kit_body, token)
    assert response.status_code == 400

# PRUEBA 1: Nombre válido
def test_create_kit_name_valid():
    positive_assert(get_kit_body("Mi kit"))

# PRUEBA 2: Nombre con 511 caracteres
def test_create_kit_name_511_chars():
    long_name = "A" * 511
    positive_assert(get_kit_body(long_name))

# PRUEBA 3: Nombre vacío (0 caracteres)
def test_create_kit_name_empty():
    negative_assert_code_400(get_kit_body(""))
# PRUEBA 4: Nombre con más de 512 caracteres
def test_create_kit_name_more_than_512_chars():
    long_name = "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD"
    negative_assert_code_400(get_kit_body(long_name))


# PRUEBA 5: Se permiten caracteres especiales
def test_create_kit_name_special_chars():
    special_name = "№%@\",\""
    body = get_kit_body(special_name)
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(body, token)

    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    response_json = response.json()
    assert response_json["name"] == special_name, f"Expected name '{special_name}', got '{response_json['name']}'"


# PRUEBA 6: Se permiten espacios
def test_create_kit_name_with_spaces():
    spaced_name = " A Aaa "
    body = get_kit_body(spaced_name)
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(body, token)

    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    response_json = response.json()
    assert response_json["name"] == spaced_name, f"Expected name '{spaced_name}', got '{response_json['name']}'"


# PRUEBA 7: Se permiten números
def test_create_kit_name_numbers():
    numeric_name = "123"
    body = get_kit_body(numeric_name)
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(body, token)

    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    response_json = response.json()
    assert response_json["name"] == numeric_name, f"Expected name '{numeric_name}', got '{response_json['name']}'"


# PRUEBA 8: El parámetro no se pasa en la solicitud
def test_create_kit_name_missing_param():
    body = {}  # sin el parámetro "name"
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(body, token)

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"


# PRUEBA 9: Se ha pasado un tipo de parámetro diferente (número)
def test_create_kit_name_wrong_type():
    body = {"name": 123}  # nombre como número en lugar de string
    token = sender_stand_request.get_new_user_token()
    response = sender_stand_request.post_new_client_kit(body, token)

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
