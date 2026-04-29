from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get(
        "/api/v1/user",
        params={"email": "unknown@mail.com"}
    )

    assert response.status_code == 404


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        "name": "Alex Smith",
        "email": "alex.smith@mail.com"
    }

    response = client.post(
        "/api/v1/user",
        json=new_user
    )

    assert response.status_code in (200, 201)

    data = response.json()

    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]
    assert "id" in data


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {
        "name": "Duplicate User",
        "email": users[0]["email"]
    }

    response = client.post(
        "/api/v1/user",
        json=duplicate_user
    )

    assert response.status_code in (400, 409)


def test_delete_user():
    '''Удаление пользователя'''
    user_to_create = {
        "name": "User To Delete",
        "email": "delete.user@mail.com"
    }

    create_response = client.post(
        "/api/v1/user",
        json=user_to_create
    )

    assert create_response.status_code in (200, 201)

    created_user = create_response.json()

    response = client.delete(
        "/api/v1/user",
        params={"email": created_user["email"]}
    )

    assert response.status_code in (200, 204)

    get_response = client.get(
        "/api/v1/user",
        params={"email": created_user["email"]}
    )

    assert get_response.status_code == 404
