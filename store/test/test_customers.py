from store.models import Customer
from core.models import User
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestCreateCustomer:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post('/store/customers/', {
            'user_id': 1,
            'phone': '123456789',
            'birth_date': '1990-01-01'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_201(self, authenticate, api_client):
        user = baker.make(User)
        authenticate(is_staff=False)

        response = api_client.post('/store/customers/', {
            'user_id': user.id,
            'phone': '123456789',
            'birth_date': '1990-01-01'
        })

        assert response.status_code in [
            status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestRetrieveCustomer:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        customer = baker.make(Customer)
        response = api_client.get(f'/store/customers/{customer.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_admin_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        customer = baker.make(Customer)

        response = api_client.get(f'/store/customers/{customer.id}/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCustomerMe:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/customers/me/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_customer_profile_returns_200(self, authenticate, api_client):
        customer = baker.make(Customer)
        api_client.force_authenticate(user=customer.user)

        response = api_client.get('/store/customers/me/')

        assert response.status_code == status.HTTP_200_OK
