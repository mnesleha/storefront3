import pytest
from core.serializers import UserCreateSerializer, UserSerializer
from core.models import User
from model_bakery import baker


@pytest.mark.django_db
class TestUserCreateSerializer:

    def test_serializer_with_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ComplexPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = UserCreateSerializer(data=data)

        assert serializer.is_valid()

    def test_serializer_with_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'ComplexPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = UserCreateSerializer(data=data)

        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_serializer_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ComplexPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        serializer = UserCreateSerializer(data=data)

        assert serializer.is_valid()
        user = serializer.save()

        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'


@pytest.mark.django_db
class TestUserSerializer:

    def test_serializer_contains_expected_fields(self):
        user = baker.make(User)
        serializer = UserSerializer(user)

        assert set(serializer.data.keys()) == {
            'id', 'username', 'email', 'first_name', 'last_name'}

    def test_serializer_data(self):
        user = baker.make(
            User,
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        serializer = UserSerializer(user)

        assert serializer.data['username'] == 'testuser'
        assert serializer.data['email'] == 'test@example.com'
        assert serializer.data['first_name'] == 'Test'
        assert serializer.data['last_name'] == 'User'
