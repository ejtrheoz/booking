from httpx import AsyncClient
import pytest
from datetime import datetime

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    *[(4, "2030-01-01", "2030-01-22", 200)]*20,
    (4, "2030-01-01", "2030-01-22", 409)
])
async def test_add_and_get_booking(room_id, date_from, date_to, status_code, authenticated_client: AsyncClient):
    response = await authenticated_client.post(
        "/bookings/add",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        })
    
    assert response.status_code == status_code


    

    # response = await client.get("/bookings/")
    # assert response.status_code == 200
    # assert len(response.json()) > 0