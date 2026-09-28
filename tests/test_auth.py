"""Unit and integration tests for authentication routes."""

import pytest


class TestRegistration:
    """Tests for the /auth/register endpoint."""

    def test_register_page_loads(self, client):
        response = client.get("/auth/register")
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_register_success(self, client, db):
        response = client.post(
            "/auth/register",
            data={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "SecurePass1",
                "confirm_password": "SecurePass1",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Registration successful" in response.data

    def test_register_duplicate_email(self, client, db, customer_user):
        response = client.post(
            "/auth/register",
            data={
                "username": "anotheruser",
                "email": customer_user.email,
                "password": "SecurePass1",
                "confirm_password": "SecurePass1",
            },
            follow_redirects=True,
        )
        assert b"Email already registered" in response.data

    def test_register_password_mismatch(self, client):
        response = client.post(
            "/auth/register",
            data={
                "username": "mismatchuser",
                "email": "mismatch@example.com",
                "password": "SecurePass1",
                "confirm_password": "WrongPass1",
            },
            follow_redirects=True,
        )
        assert b"Passwords must match" in response.data

    def test_register_short_password(self, client):
        response = client.post(
            "/auth/register",
            data={
                "username": "shortpw",
                "email": "shortpw@example.com",
                "password": "abc",
                "confirm_password": "abc",
            },
            follow_redirects=True,
        )
        assert b"at least 8 characters" in response.data


class TestLogin:
    """Tests for the /auth/login endpoint."""

    def test_login_page_loads(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_login_success(self, client, db, customer_user):
        response = client.post(
            "/auth/login",
            data={
                "email": customer_user.email,
                "password": "TestPass@1",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Welcome back" in response.data

    def test_login_wrong_password(self, client, db, customer_user):
        response = client.post(
            "/auth/login",
            data={
                "email": customer_user.email,
                "password": "WrongPassword",
            },
            follow_redirects=True,
        )
        assert b"Invalid email or password" in response.data

    def test_login_nonexistent_email(self, client):
        response = client.post(
            "/auth/login",
            data={
                "email": "nobody@nowhere.com",
                "password": "SomePass1",
            },
            follow_redirects=True,
        )
        assert b"Invalid email or password" in response.data


class TestLogout:
    """Tests for the /auth/logout endpoint."""

    def test_logout_redirects(self, client, db, customer_user):
        # Log in first
        client.post(
            "/auth/login",
            data={
                "email": customer_user.email,
                "password": "TestPass@1",
            },
        )
        response = client.get("/auth/logout", follow_redirects=True)
        assert response.status_code == 200
        assert b"logged out" in response.data

    def test_logout_requires_login(self, client):
        """Unauthenticated logout redirects to login page."""
        response = client.get("/auth/logout")
        assert response.status_code == 302


class TestRoleAccess:
    """Tests for role-based access control."""

    def test_admin_dashboard_requires_auth(self, client):
        response = client.get("/admin/")
        # Redirected to login
        assert response.status_code == 302

    def test_admin_dashboard_forbidden_for_customer(self, client, db, customer_user):
        client.post(
            "/auth/login",
            data={
                "email": customer_user.email,
                "password": "TestPass@1",
            },
        )
        response = client.get("/admin/", follow_redirects=True)
        assert response.status_code == 403

    def test_admin_dashboard_accessible_for_admin(self, client, db, admin_user):
        client.post(
            "/auth/login",
            data={
                "email": admin_user.email,
                "password": "AdminPass@1",
            },
        )
        response = client.get("/admin/")
        assert response.status_code == 200
        assert b"Dashboard" in response.data
