from starlette import status
from httpx import AsyncClient

user_data_1 = {
    "username": "logintest",
    "email": "logintest@gmail.com",
    "password": "string"
}

invalid_login_data = {
    "email": "wrong@gmail.com",
    "password": "string"
}


def test_auth(client):
    client.post("/register/", json=user_data_1)
    response = client.post("/login/", json=invalid_login_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.post("/login/", json=user_data_1)
    assert response.status_code == status.HTTP_200_OK


async def test_logout(ac: AsyncClient):
    response = await ac.delete("/logout/")
    response.status_code == status.HTTP_200_OK
