from store.models import Review, Product, Collection
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestCreateReview:

    def test_returns_201(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        response = api_client.post(f'/store/products/{product.id}/reviews/', {
            'name': 'Test Reviewer',
            'description': 'Great product!'
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Reviewer'

    def test_if_data_is_invalid_returns_400(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        response = api_client.post(f'/store/products/{product.id}/reviews/', {
            'name': '',
            'description': ''
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListReviews:

    def test_returns_200(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        baker.make(Review, product=product, _quantity=3)

        response = api_client.get(f'/store/products/{product.id}/reviews/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


@pytest.mark.django_db
class TestRetrieveReview:

    def test_if_review_exists_returns_200(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        review = baker.make(Review, product=product)

        response = api_client.get(
            f'/store/products/{product.id}/reviews/{review.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == review.id


@pytest.mark.django_db
class TestUpdateReview:

    def test_returns_200(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        review = baker.make(Review, product=product)

        response = api_client.patch(f'/store/products/{product.id}/reviews/{review.id}/', {
            'name': 'Updated Name'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Name'


@pytest.mark.django_db
class TestDeleteReview:

    def test_returns_204(self, api_client):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        review = baker.make(Review, product=product)

        response = api_client.delete(
            f'/store/products/{product.id}/reviews/{review.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
