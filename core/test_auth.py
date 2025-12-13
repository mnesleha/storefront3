import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from core.models import User
from store.models import Customer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestUserRegistration:

    def test_create_user_returns_201(self, api_client):
        response = api_client.post('/auth/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'ComplexPass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['username'] == 'newuser'
        assert response.data['email'] == 'newuser@example.com'

    def test_create_user_with_invalid_email_returns_400(self, api_client):
        response = api_client.post('/auth/users/', {
            'username': 'newuser',
            'email': 'invalid-email',
            'password': 'ComplexPass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_with_existing_email_returns_400(self, api_client):
        baker.make(User, email='existing@example.com', username='existing')

        response = api_client.post('/auth/users/', {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'ComplexPass123!',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_without_password_returns_400(self, api_client):
        response = api_client.post('/auth/users/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfile:

    def test_retrieve_current_user_returns_200(self, api_client):
        user = baker.make(User, username='currentuser',
                          email='current@example.com')
        api_client.force_authenticate(user=user)

        response = api_client.get('/auth/users/me/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'currentuser'
        assert response.data['email'] == 'current@example.com'

    def test_retrieve_current_user_unauthenticated_returns_401(self, api_client):
        response = api_client.get('/auth/users/me/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_current_user_returns_200(self, api_client):
        user = baker.make(User, username='currentuser',
                          email='current@example.com')
        api_client.force_authenticate(user=user)

        response = api_client.patch('/auth/users/me/', {
            'first_name': 'Updated',
            'last_name': 'Name'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
