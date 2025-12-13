import pytest
from model_bakery import baker
from core.models import User


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = baker.make(User, email='test@example.com', username='testuser')

        assert user.id is not None
        assert user.email == 'test@example.com'
        assert user.username == 'testuser'

    def test_user_email_is_unique(self):
        baker.make(User, email='test@example.com', username='user1')

        with pytest.raises(Exception):
            User.objects.create(
                email='test@example.com',
                username='user2',
                password='password123'
            )

    def test_user_string_representation(self):
        user = baker.make(User, username='johndoe')

        assert str(user) == 'johndoe'

    def test_user_has_email_field(self):
        user = baker.make(User)

        assert hasattr(user, 'email')

    def test_user_inherits_from_abstract_user(self):
        user = baker.make(User)

        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')
        assert hasattr(user, 'is_staff')
        assert hasattr(user, 'is_active')


@pytest.mark.django_db
class TestUserPermissions:

    def test_user_is_staff_default_false(self):
        user = baker.make(User)

        assert user.is_staff is False

    def test_user_is_active_default_true(self):
        user = baker.make(User)

        assert user.is_active is True

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

        assert user.is_staff is True
        assert user.is_superuser is True
