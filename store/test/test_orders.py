from store.models import Order, OrderItem, Customer, Cart, CartItem, Product, Collection
from core.models import User
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestCreateOrder:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.post(
            '/store/orders/', {'cart_id': 'test-cart-id'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_no_customer_profile_returns_400(self, authenticate, api_client):
        user = baker.make(User)
        api_client.force_authenticate(user=user)
        cart = baker.make(Cart)

        response = api_client.post('/store/orders/', {'cart_id': str(cart.id)})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_cart_is_empty_returns_400(self, authenticate, api_client):
        customer = baker.make(Customer)
        api_client.force_authenticate(user=customer.user)
        cart = baker.make(Cart)

        response = api_client.post('/store/orders/', {'cart_id': str(cart.id)})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, authenticate, api_client):
        customer = baker.make(Customer)
        api_client.force_authenticate(user=customer.user)
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection, unit_price=10)
        baker.make(CartItem, cart=cart, product=product, quantity=2)

        response = api_client.post('/store/orders/', {'cart_id': str(cart.id)})

        assert response.status_code in [
            status.HTTP_200_OK, status.HTTP_201_CREATED]
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveOrder:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/orders/1/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_retrieves_own_order_returns_200(self, api_client):
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)
        api_client.force_authenticate(user=customer.user)

        response = api_client.get(f'/store/orders/{order.id}/')

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUpdateOrder:

    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate(is_staff=False)
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)

        response = api_client.patch(f'/store/orders/{order.id}/', {
            'payment_status': 'C'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)

        response = api_client.patch(f'/store/orders/{order.id}/', {
            'payment_status': 'C'
        })

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestListOrders:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        response = api_client.get('/store/orders/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_authenticated_returns_200(self, api_client):
        customer = baker.make(Customer)
        api_client.force_authenticate(user=customer.user)

        response = api_client.get('/store/orders/')

        assert response.status_code == status.HTTP_200_OK
