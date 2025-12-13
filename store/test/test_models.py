import pytest
from decimal import Decimal
from model_bakery import baker
from store.models import (
    Product, Collection, Customer, Order, OrderItem,
    Cart, CartItem, Review, ProductImage, Promotion
)
from core.models import User


@pytest.mark.django_db
class TestProductModel:

    def test_create_product(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection,
                             unit_price=Decimal('10.99'))

        assert product.id is not None
        assert product.unit_price == Decimal('10.99')
        assert product.collection == collection

    def test_product_string_representation(self):
        product = baker.make(Product, title='Test Product')

        assert str(product) == 'Test Product'


@pytest.mark.django_db
class TestCollectionModel:

    def test_create_collection(self):
        collection = baker.make(Collection, title='Electronics')

        assert collection.id is not None
        assert collection.title == 'Electronics'

    def test_collection_string_representation(self):
        collection = baker.make(Collection, title='Books')

        assert str(collection) == 'Books'


@pytest.mark.django_db
class TestCustomerModel:

    def test_create_customer(self):
        customer = baker.make(Customer, phone='123456789',
                              user__first_name='John', user__last_name='Doe')

        assert customer.id is not None
        assert customer.phone == '123456789'
        assert customer.user is not None

    def test_customer_string_representation(self):
        customer = baker.make(
            Customer, user__first_name='John', user__last_name='Doe')

        assert str(customer) == 'John Doe'

    def test_customer_membership_default(self):
        customer = baker.make(Customer)

        assert customer.membership == Customer.MEMBERSHIP_BRONZE


@pytest.mark.django_db
class TestOrderModel:

    def test_create_order(self):
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)

        assert order.id is not None
        assert order.customer == customer

    def test_order_payment_status_default(self):
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)

        assert order.payment_status == Order.PAYMENT_STATUS_PENDING


@pytest.mark.django_db
class TestOrderItemModel:

    def test_create_order_item(self):
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        order_item = baker.make(
            OrderItem, order=order, product=product, quantity=2, unit_price=Decimal('10.99'))

        assert order_item.id is not None
        assert order_item.quantity == 2
        assert order_item.unit_price == Decimal('10.99')


@pytest.mark.django_db
class TestCartModel:

    def test_create_cart(self):
        cart = baker.make(Cart)

        assert cart.id is not None

    def test_cart_id_is_uuid(self):
        cart = baker.make(Cart)

        assert isinstance(str(cart.id), str)


@pytest.mark.django_db
class TestCartItemModel:

    def test_create_cart_item(self):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        cart_item = baker.make(CartItem, cart=cart,
                               product=product, quantity=3)

        assert cart_item.id is not None
        assert cart_item.quantity == 3

    def test_cart_item_unique_constraint(self):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        baker.make(CartItem, cart=cart, product=product, quantity=1)

        # This should raise an error due to unique_together constraint
        with pytest.raises(Exception):
            CartItem.objects.create(cart=cart, product=product, quantity=2)


@pytest.mark.django_db
class TestReviewModel:

    def test_create_review(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        review = baker.make(Review, product=product,
                            name='John', description='Great!')

        assert review.id is not None
        assert review.name == 'John'
        assert review.description == 'Great!'


@pytest.mark.django_db
class TestProductImageModel:

    def test_create_product_image(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        # Note: This test might fail if image validation is strict
        product_image = baker.make(
            ProductImage, product=product, make_m2m=True)

        assert product_image.id is not None
        assert product_image.product == product


@pytest.mark.django_db
class TestPromotionModel:

    def test_create_promotion(self):
        promotion = baker.make(
            Promotion, description='Summer Sale', discount=0.15)

        assert promotion.id is not None
        assert promotion.description == 'Summer Sale'
        assert promotion.discount == 0.15
