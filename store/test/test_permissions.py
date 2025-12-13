import pytest
from unittest.mock import Mock
from rest_framework.test import APIRequestFactory
from store.permissions import (
    IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission
)
from core.models import User
from model_bakery import baker


@pytest.fixture
def api_factory():
    return APIRequestFactory()


@pytest.mark.django_db
class TestIsAdminOrReadOnly:

    def test_allows_safe_methods_for_anonymous_users(self, api_factory):
        permission = IsAdminOrReadOnly()
        request = api_factory.get('/')
        request.user = None

        assert permission.has_permission(request, None) is True

    def test_allows_safe_methods_for_authenticated_non_admin(self, api_factory):
        permission = IsAdminOrReadOnly()
        user = baker.make(User, is_staff=False)
        request = api_factory.get('/')
        request.user = user

        assert permission.has_permission(request, None) is True

    def test_denies_unsafe_methods_for_anonymous_users(self, api_factory):
        permission = IsAdminOrReadOnly()
        request = api_factory.post('/')
        request.user = None

        assert permission.has_permission(request, None) is False

    def test_denies_unsafe_methods_for_non_admin_users(self, api_factory):
        permission = IsAdminOrReadOnly()
        user = baker.make(User, is_staff=False)
        request = api_factory.post('/')
        request.user = user

        assert permission.has_permission(request, None) is False

    def test_allows_unsafe_methods_for_admin_users(self, api_factory):
        permission = IsAdminOrReadOnly()
        user = baker.make(User, is_staff=True)
        request = api_factory.post('/')
        request.user = user

        assert permission.has_permission(request, None) is True

    def test_allows_get_request(self, api_factory):
        permission = IsAdminOrReadOnly()
        request = api_factory.get('/')
        request.user = baker.make(User, is_staff=False)

        assert permission.has_permission(request, None) is True

    def test_allows_head_request(self, api_factory):
        permission = IsAdminOrReadOnly()
        request = api_factory.head('/')
        request.user = baker.make(User, is_staff=False)

        assert permission.has_permission(request, None) is True

    def test_allows_options_request(self, api_factory):
        permission = IsAdminOrReadOnly()
        request = api_factory.options('/')
        request.user = baker.make(User, is_staff=False)

        assert permission.has_permission(request, None) is True

    def test_denies_put_for_non_admin(self, api_factory):
        permission = IsAdminOrReadOnly()
        user = baker.make(User, is_staff=False)
        request = api_factory.put('/')
        request.user = user

        assert permission.has_permission(request, None) is False

    def test_denies_patch_for_non_admin(self, api_factory):
        permission = IsAdminOrReadOnly()
        user = baker.make(User, is_staff=False)
        request = api_factory.patch('/')
        request.user = user

        assert permission.has_permission(request, None) is False

    def test_denies_delete_for_non_admin(self, api_factory):
        permission = IsAdminOrReadOnly()
        user = baker.make(User, is_staff=False)
        request = api_factory.delete('/')
        request.user = user

        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestFullDjangoModelPermissions:

    def test_permission_initialization(self):
        permission = FullDjangoModelPermissions()

        assert 'GET' in permission.perms_map

    def test_get_method_requires_view_permission(self):
        permission = FullDjangoModelPermissions()

        assert permission.perms_map['GET'] == [
            '%(app_label)s.view_%(model_name)s']


@pytest.mark.django_db
class TestViewCustomerHistoryPermission:

    def test_allows_user_with_permission(self, api_factory):
        permission = ViewCustomerHistoryPermission()
        user = baker.make(User)

        # Mock the has_perm method
        user.has_perm = Mock(return_value=True)

        request = api_factory.get('/')
        request.user = user

        assert permission.has_permission(request, None) is True

    def test_denies_user_without_permission(self, api_factory):
        permission = ViewCustomerHistoryPermission()
        user = baker.make(User)

        # Mock the has_perm method
        user.has_perm = Mock(return_value=False)

        request = api_factory.get('/')
        request.user = user

        assert permission.has_permission(request, None) is False

    def test_checks_correct_permission(self, api_factory):
        permission = ViewCustomerHistoryPermission()
        user = baker.make(User)

        user.has_perm = Mock(return_value=True)

        request = api_factory.get('/')
        request.user = user

        permission.has_permission(request, None)

        user.has_perm.assert_called_once_with('store.view_history')
