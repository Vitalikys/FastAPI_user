# https://www.youtube.com/watch?v=7dgQRVqF1N0&ab_channel=pixegami
import requests

# ENDPOINT = 'http://78.27.202.55:8003'
ENDPOINT = 'http://127.0.0.1:8000'


def test_can_call_endpoint():
    response = requests.get(ENDPOINT + '/docs')
    assert response.status_code == 200


def test_create_user():
    payload = new_user_payload()
    create_user_response = requests.post(ENDPOINT + '/create_user', json=payload)
    assert create_user_response.status_code == 200

    data = create_user_response.json()
    new_user_id = data['new_user id']

    # "get" last created user:
    get_user_response = requests.get(ENDPOINT + f'/user/{new_user_id}')
    get_user_data = get_user_response.json()

    assert get_user_response.status_code == 200
    assert get_user_data['email'] == payload['user']['email']
    print('get_user_data: ', get_user_data)

    # delete last created user
    delete_user_response = requests.delete(ENDPOINT + f'/user_delete/{new_user_id}')
    assert delete_user_response.status_code == 200


def new_user_payload():
    return {
        "user": {
            "firstname": "from schemas",
            "email": "user_from_test_user_create--0@example.com",
            "password": "string",
            "age": 18
        }
    }
