import pytest
from core.db import create_conn
from core.models import User


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a', 'email': 'a@mail.com'}
    )
    assert response.headers["Location"] == "/auth/login"

    cnx, cursor = create_conn(testing=True)
    assert User.load_user_by_username(cursor, 'a') is not None
    cnx.close()



@pytest.mark.parametrize(('username', 'password', 'email', 'message'), (
    ('', '', '', b'Username is required.'),
    ('a', '', '', b'Password is required.'),
    ('a', 'b', '', b'Email is required'),
    ('test', 'test', 'test@mail.com', b'already registered'),
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'email': email}
    )
    assert message in response.data