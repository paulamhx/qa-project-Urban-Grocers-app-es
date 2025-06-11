import requests
import configuration
import data


# Crear nuevo usuario y devolver token
def get_new_user_token():
    response = requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                             json=data.user_body)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create user: {response.status_code} - {response.text}")

    try:
        return response.json()["authToken"]
    except ValueError as e:
        raise Exception(f"Invalid JSON response: {response.text}") from e


# Crear nuevo kit con nombre y token
def post_new_client_kit(kit_body, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(configuration.URL_SERVICE + configuration.KITS_PATH,
                             json=kit_body, headers=headers)
    return response
