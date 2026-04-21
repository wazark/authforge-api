def test_register(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test1@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["email"] == "test1@test.com"

def test_login(client):
    # First create user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@test.com",
            "password": "123456"
        }
    )

    # Then login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data

def test_get_me(client):
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "me@test.com",
            "password": "123456"
        }
    )

    # Login
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "me@test.com",
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    # Access protected route
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "me@test.com"

def test_invalid_login(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@test.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401
    
def test_logout_invalidates_token(client):
    
    # 1. Register
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "logout@test.com",
            "password": "123456"
        }
    )

    
    # 2. Login
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "logout@test.com",
            "password": "123456"
        }
    )

    data = login.json()
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    
    # 3. Access protected route (should work)
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200

    
    # 4. Logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
        headers=headers
    )

    assert logout_response.status_code == 200

    
    # 5. Try to access again (should fail)
    response_after_logout = client.get(
        "/api/v1/auth/me",
        headers=headers
    )

    assert response_after_logout.status_code == 401
    assert response_after_logout.json()["detail"] in [
        "Token revoked",
        "Invalid authentication credentials"
    ]