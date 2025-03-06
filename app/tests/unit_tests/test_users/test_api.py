from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("comp@gmail.com", "test_password", 200),
    ("vasya@gmail.com", "test_password", 409),
    ("abcde", "pesokot", 422),
])
async def test_register_user(email, password, status_code, client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        })
    
    assert response.status_code == status_code

@pytest.mark.parametrize("email, password, status_code", [
    ("vasya@example.com", "ejer", 200)
])
async def test_login_user(email, password, status_code, client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        })

    assert response.status_code == status_code