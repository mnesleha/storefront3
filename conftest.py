import pytest
from django.db.models.signals import post_save
from django.conf import settings


@pytest.fixture(autouse=True)
def disable_customer_creation_signal(db):
    """Disable the automatic customer creation signal during tests."""
    from store.signals.handlers import create_customer_for_new_user

    post_save.disconnect(create_customer_for_new_user,
                         sender=settings.AUTH_USER_MODEL)
    yield
    post_save.connect(create_customer_for_new_user,
                      sender=settings.AUTH_USER_MODEL)
