import pytest
from model_bakery import baker
from store.filters import ProductFilter
from store.models import Product, Collection
from decimal import Decimal


@pytest.mark.django_db
class TestProductFilter:

    def test_filter_by_collection_id(self):
        collection1 = baker.make(Collection)
        collection2 = baker.make(Collection)

        product1 = baker.make(Product, collection=collection1)
        product2 = baker.make(Product, collection=collection1)
        product3 = baker.make(Product, collection=collection2)

        filter_set = ProductFilter(
            data={'collection_id': collection1.id},
            queryset=Product.objects.all()
        )

        assert filter_set.is_valid()
        filtered_products = filter_set.qs

        assert product1 in filtered_products
        assert product2 in filtered_products
        assert product3 not in filtered_products

    def test_filter_by_unit_price_greater_than(self):
        collection = baker.make(Collection)

        product1 = baker.make(Product, collection=collection,
                              unit_price=Decimal('10.00'))
        product2 = baker.make(Product, collection=collection,
                              unit_price=Decimal('20.00'))
        product3 = baker.make(Product, collection=collection,
                              unit_price=Decimal('30.00'))

        filter_set = ProductFilter(
            data={'unit_price__gt': '15.00'},
            queryset=Product.objects.all()
        )

        assert filter_set.is_valid()
        filtered_products = filter_set.qs

        assert product1 not in filtered_products
        assert product2 in filtered_products
        assert product3 in filtered_products

    def test_filter_by_unit_price_less_than(self):
        collection = baker.make(Collection)

        product1 = baker.make(Product, collection=collection,
                              unit_price=Decimal('10.00'))
        product2 = baker.make(Product, collection=collection,
                              unit_price=Decimal('20.00'))
        product3 = baker.make(Product, collection=collection,
                              unit_price=Decimal('30.00'))

        filter_set = ProductFilter(
            data={'unit_price__lt': '25.00'},
            queryset=Product.objects.all()
        )

        assert filter_set.is_valid()
        filtered_products = filter_set.qs

        assert product1 in filtered_products
        assert product2 in filtered_products
        assert product3 not in filtered_products

    def test_filter_by_multiple_criteria(self):
        collection1 = baker.make(Collection)
        collection2 = baker.make(Collection)

        product1 = baker.make(
            Product, collection=collection1, unit_price=Decimal('10.00'))
        product2 = baker.make(
            Product, collection=collection1, unit_price=Decimal('20.00'))
        product3 = baker.make(
            Product, collection=collection2, unit_price=Decimal('15.00'))

        filter_set = ProductFilter(
            data={
                'collection_id': collection1.id,
                'unit_price__gt': '5.00',
                'unit_price__lt': '25.00'
            },
            queryset=Product.objects.all()
        )

        assert filter_set.is_valid()
        filtered_products = filter_set.qs

        assert product1 in filtered_products
        assert product2 in filtered_products
        assert product3 not in filtered_products

    def test_filter_with_no_criteria(self):
        collection = baker.make(Collection)

        product1 = baker.make(Product, collection=collection)
        product2 = baker.make(Product, collection=collection)

        filter_set = ProductFilter(
            data={},
            queryset=Product.objects.all()
        )

        assert filter_set.is_valid()
        filtered_products = filter_set.qs

        assert product1 in filtered_products
        assert product2 in filtered_products

    def test_filter_returns_empty_when_no_match(self):
        collection = baker.make(Collection)
        baker.make(Product, collection=collection, unit_price=Decimal('10.00'))

        filter_set = ProductFilter(
            data={'unit_price__gt': '100.00'},
            queryset=Product.objects.all()
        )

        assert filter_set.is_valid()
        filtered_products = filter_set.qs

        assert filtered_products.count() == 0
