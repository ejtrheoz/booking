import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id, email, is_present", [
    (1, "vasya@gmail.com", True),
    (2, "vasya@example.com", True),
    (3, "asasa", False),
])
async def test_find_one_or_none(user_id, email, is_present):
    user = await UsersDAO.find_one_or_none(id=user_id, email=email)

    if is_present:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user