from store.models import Product, Collection, OrderItem
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture
def create_product(api_client):
    def do_create_product(product_data):
        return api_client.post('/store/products/', product_data)
    return do_create_product


@pytest.mark.django_db
class TestCreateProduct:

    @pytest.mark.smoke
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product):
        collection = baker.make(Collection)
        response = create_product({
            'title': 'Test Product',
            'slug': 'test-product',
            'unit_price': 10.99,
            'inventory': 10,
            'collection': collection.id
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.smoke
    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate(is_staff=False)
        collection = baker.make(Collection)
        response = create_product({
            'title': 'Test Product',
            'slug': 'test-product',
            'unit_price': 10.99,
            'inventory': 10,
            'collection': collection.id
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.smoke
    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)
        response = create_product({'title': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.regression
    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        response = create_product({
            'title': 'Test Product',
            'slug': 'test-product',
            'unit_price': 10.99,
            'inventory': 10,
            'collection': collection.id
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['title'] == 'Test Product'


@pytest.mark.django_db
class TestRetrieveProduct:
    pytestmark = [pytest.mark.slow, pytest.mark.webtest]

    def test_if_product_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.get(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title

    def test_if_product_not_exists_returns_404(self, api_client):
        response = api_client.get('/store/products/999/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateProduct:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.patch(f'/store/products/{product.id}/', {
            'title': 'Updated Product'
        })

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate(is_staff=False)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.patch(f'/store/products/{product.id}/', {
            'title': 'Updated Product'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.patch(f'/store/products/{product.id}/', {
            'title': 'Updated Product'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Product'


@pytest.mark.django_db
class TestDeleteProduct:

    def test_if_user_is_anonymous_returns_401(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
        authenticate(is_staff=False)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_has_order_items_returns_405(self, authenticate, api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        baker.make(OrderItem, product=product)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_if_product_has_no_order_items_returns_204(self, authenticate, api_client):
        authenticate(is_staff=True)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        response = api_client.delete(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestListProducts:

    def test_returns_200(self, api_client):
        response = api_client.get('/store/products/')

        assert response.status_code == status.HTTP_200_OK

    def test_returns_products_list(self, api_client):
        collection = baker.make(Collection)
        baker.make(Product, collection=collection, _quantity=3)

        response = api_client.get('/store/products/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3
