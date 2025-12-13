from store.models import Cart, CartItem, Product, Collection
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestCreateCart:

    def test_returns_201(self, api_client):
        response = api_client.post('/store/carts/', {})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None


@pytest.mark.django_db
class TestRetrieveCart:

    def test_if_cart_exists_returns_200(self, api_client):
        cart = baker.make(Cart)
        response = api_client.get(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == str(cart.id)

    def test_if_cart_not_exists_returns_404(self, api_client):
        response = api_client.get(
            '/store/carts/11111111-1111-1111-1111-111111111111/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCart:

    def test_returns_204(self, api_client):
        cart = baker.make(Cart)
        response = api_client.delete(f'/store/carts/{cart.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestCartItems:

    def test_add_item_to_cart_returns_201(self, api_client):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        response = api_client.post(f'/store/carts/{cart.id}/items/', {
            'product_id': product.id,
            'quantity': 1
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None
        assert response.data['quantity'] == 1

    def test_add_item_with_invalid_product_returns_400(self, api_client):
        cart = baker.make(Cart)

        response = api_client.post(f'/store/carts/{cart.id}/items/', {
            'product_id': 999,
            'quantity': 1
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_cart_item_returns_200(self, api_client):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        cart_item = baker.make(CartItem, cart=cart,
                               product=product, quantity=1)

        response = api_client.patch(f'/store/carts/{cart.id}/items/{cart_item.id}/', {
            'quantity': 5
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity'] == 5

    def test_delete_cart_item_returns_204(self, api_client):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        cart_item = baker.make(CartItem, cart=cart,
                               product=product, quantity=1)

        response = api_client.delete(
            f'/store/carts/{cart.id}/items/{cart_item.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_cart_items_returns_200(self, api_client):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product1 = baker.make(Product, collection=collection)
        product2 = baker.make(Product, collection=collection)
        baker.make(CartItem, cart=cart, product=product1, quantity=1)
        baker.make(CartItem, cart=cart, product=product2, quantity=2)

        response = api_client.get(f'/store/carts/{cart.id}/items/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
