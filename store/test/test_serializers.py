import pytest
from decimal import Decimal
from model_bakery import baker
from store.serializers import (
    CollectionSerializer, ProductSerializer, ReviewSerializer,
    CartSerializer, CartItemSerializer, AddCartItemSerializer,
    UpdateCartItemSerializer, CustomerSerializer, OrderSerializer,
    OrderItemSerializer, CreateOrderSerializer, UpdateOrderSerializer,
    SimpleProductSerializer, ProductImageSerializer
)
from store.models import (
    Collection, Product, Review, Cart, CartItem, Customer, Order, OrderItem
)
from core.models import User


@pytest.mark.django_db
class TestCollectionSerializer:

    def test_serializer_contains_expected_fields(self):
        collection = Collection.objects.create(title='Test Collection')
        serializer = CollectionSerializer(collection)
        data = serializer.data

        assert 'id' in data
        assert 'title' in data
        assert data['title'] == 'Test Collection'

    def test_products_count_is_read_only(self):
        data = {'title': 'Test Collection', 'products_count': 100}
        serializer = CollectionSerializer(data=data)

        assert serializer.is_valid()
        # products_count should be ignored when creating


@pytest.mark.django_db
class TestProductSerializer:

    def test_serializer_contains_expected_fields(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        serializer = ProductSerializer(product)

        expected_fields = {
            'id', 'title', 'description', 'slug', 'inventory',
            'unit_price', 'price_with_tax', 'collection', 'images'
        }
        assert set(serializer.data.keys()) == expected_fields

    def test_price_with_tax_calculation(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection,
                             unit_price=Decimal('100.00'))
        serializer = ProductSerializer(product)

        expected_price_with_tax = Decimal('100.00') * Decimal('1.1')
        actual_price = Decimal(serializer.data['price_with_tax'])
        # Allow for small floating point differences
        assert abs(actual_price - expected_price_with_tax) < Decimal('0.01')


@pytest.mark.django_db
class TestSimpleProductSerializer:

    def test_serializer_contains_only_simple_fields(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        serializer = SimpleProductSerializer(product)

        assert set(serializer.data.keys()) == {'id', 'title', 'unit_price'}


@pytest.mark.django_db
class TestReviewSerializer:

    def test_serializer_contains_expected_fields(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        review = baker.make(Review, product=product)
        serializer = ReviewSerializer(review)

        assert set(serializer.data.keys()) == {
            'id', 'date', 'name', 'description'}

    def test_create_review_with_product_context(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        data = {'name': 'Test User', 'description': 'Great product!'}

        serializer = ReviewSerializer(
            data=data, context={'product_id': product.id})
        assert serializer.is_valid()
        review = serializer.save()

        assert review.product == product


@pytest.mark.django_db
class TestCartSerializer:

    def test_serializer_contains_expected_fields(self):
        cart = baker.make(Cart)
        serializer = CartSerializer(cart)

        assert set(serializer.data.keys()) == {'id', 'items', 'total_price'}

    def test_cart_id_is_read_only(self):
        cart = baker.make(Cart)
        serializer = CartSerializer(cart)

        assert 'id' in serializer.data


@pytest.mark.django_db
class TestCartItemSerializer:

    def test_serializer_contains_expected_fields(self):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        cart_item = baker.make(CartItem, cart=cart, product=product)
        serializer = CartItemSerializer(cart_item)

        assert set(serializer.data.keys()) == {
            'id', 'product', 'quantity', 'total_price'}

    def test_total_price_calculation(self):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection,
                             unit_price=Decimal('10.00'))
        cart_item = baker.make(CartItem, cart=cart,
                               product=product, quantity=3)
        serializer = CartItemSerializer(cart_item)

        assert Decimal(serializer.data['total_price']) == Decimal('30.00')


@pytest.mark.django_db
class TestAddCartItemSerializer:

    def test_validate_product_id_with_valid_product(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        cart = baker.make(Cart)

        data = {'product_id': product.id, 'quantity': 1}
        serializer = AddCartItemSerializer(
            data=data, context={'cart_id': cart.id})

        assert serializer.is_valid()

    def test_validate_product_id_with_invalid_product(self):
        cart = baker.make(Cart)
        data = {'product_id': 9999, 'quantity': 1}
        serializer = AddCartItemSerializer(
            data=data, context={'cart_id': cart.id})

        assert not serializer.is_valid()
        assert 'product_id' in serializer.errors


@pytest.mark.django_db
class TestCustomerSerializer:

    def test_serializer_contains_expected_fields(self):
        customer = baker.make(Customer)
        serializer = CustomerSerializer(customer)

        expected_fields = {'id', 'user_id',
                           'phone', 'birth_date', 'membership'}
        assert set(serializer.data.keys()) == expected_fields

    def test_user_id_is_read_only(self):
        serializer = CustomerSerializer()
        user_id_field = serializer.fields['user_id']

        assert user_id_field.read_only is True


@pytest.mark.django_db
class TestOrderSerializer:

    def test_serializer_contains_expected_fields(self):
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer)
        serializer = OrderSerializer(order)

        expected_fields = {'id', 'customer',
                           'placed_at', 'payment_status', 'items'}
        assert set(serializer.data.keys()) == expected_fields


@pytest.mark.django_db
class TestCreateOrderSerializer:

    def test_validate_cart_id_with_valid_cart(self):
        cart = baker.make(Cart)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        baker.make(CartItem, cart=cart, product=product)

        data = {'cart_id': cart.id}
        serializer = CreateOrderSerializer(data=data)

        assert serializer.is_valid()

    def test_validate_cart_id_with_nonexistent_cart(self):
        data = {'cart_id': '11111111-1111-1111-1111-111111111111'}
        serializer = CreateOrderSerializer(data=data)

        assert not serializer.is_valid()
        assert 'cart_id' in serializer.errors

    def test_validate_cart_id_with_empty_cart(self):
        cart = baker.make(Cart)
        data = {'cart_id': cart.id}
        serializer = CreateOrderSerializer(data=data)

        assert not serializer.is_valid()
        assert 'cart_id' in serializer.errors


@pytest.mark.django_db
class TestUpdateOrderSerializer:

    def test_serializer_contains_only_payment_status(self):
        serializer = UpdateOrderSerializer()

        assert set(serializer.fields.keys()) == {'payment_status'}

    def test_update_payment_status(self):
        customer = baker.make(Customer)
        order = baker.make(Order, customer=customer, payment_status='P')

        data = {'payment_status': 'C'}
        serializer = UpdateOrderSerializer(order, data=data)

        assert serializer.is_valid()
        updated_order = serializer.save()

        assert updated_order.payment_status == 'C'
