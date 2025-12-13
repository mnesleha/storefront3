import pytest
from model_bakery import baker
from django.contrib.contenttypes.models import ContentType
from likes.models import LikedItem
from core.models import User
from store.models import Product, Collection


@pytest.mark.django_db
class TestLikedItemModel:

    def test_create_liked_item(self):
        user = baker.make(User)
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        liked_item = LikedItem.objects.create(
            user=user,
            content_type=content_type,
            object_id=collection.id
        )

        assert liked_item.id is not None
        assert liked_item.user == user
        assert liked_item.content_object == collection

    def test_liked_item_with_product(self):
        user = baker.make(User)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        content_type = ContentType.objects.get_for_model(Product)

        liked_item = LikedItem.objects.create(
            user=user,
            content_type=content_type,
            object_id=product.id
        )

        assert liked_item.content_object == product
        assert isinstance(liked_item.content_object, Product)

    def test_liked_item_with_collection(self):
        user = baker.make(User)
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        liked_item = LikedItem.objects.create(
            user=user,
            content_type=content_type,
            object_id=collection.id
        )

        assert liked_item.content_object == collection
        assert isinstance(liked_item.content_object, Collection)

    def test_user_can_like_multiple_items(self):
        user = baker.make(User)
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        collection_ct = ContentType.objects.get_for_model(Collection)
        product_ct = ContentType.objects.get_for_model(Product)

        LikedItem.objects.create(
            user=user, content_type=collection_ct, object_id=collection.id)
        LikedItem.objects.create(
            user=user, content_type=product_ct, object_id=product.id)

        user_likes = LikedItem.objects.filter(user=user)

        assert user_likes.count() == 2

    def test_multiple_users_can_like_same_item(self):
        user1 = baker.make(User)
        user2 = baker.make(User)
        user3 = baker.make(User)
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        LikedItem.objects.create(
            user=user1, content_type=content_type, object_id=collection.id)
        LikedItem.objects.create(
            user=user2, content_type=content_type, object_id=collection.id)
        LikedItem.objects.create(
            user=user3, content_type=content_type, object_id=collection.id)

        item_likes = LikedItem.objects.filter(
            content_type=content_type,
            object_id=collection.id
        )

        assert item_likes.count() == 3

    def test_get_user_likes(self):
        user = baker.make(User)
        collection1 = baker.make(Collection)
        collection2 = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        LikedItem.objects.create(
            user=user, content_type=content_type, object_id=collection1.id)
        LikedItem.objects.create(
            user=user, content_type=content_type, object_id=collection2.id)

        user_likes = LikedItem.objects.filter(user=user)

        assert user_likes.count() == 2

    def test_get_item_likes_count(self):
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        user1 = baker.make(User)
        user2 = baker.make(User)

        LikedItem.objects.create(
            user=user1, content_type=content_type, object_id=collection.id)
        LikedItem.objects.create(
            user=user2, content_type=content_type, object_id=collection.id)

        likes_count = LikedItem.objects.filter(
            content_type=content_type,
            object_id=collection.id
        ).count()

        assert likes_count == 2

    def test_unlike_item(self):
        user = baker.make(User)
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        liked_item = LikedItem.objects.create(
            user=user,
            content_type=content_type,
            object_id=collection.id
        )

        liked_item.delete()

        assert LikedItem.objects.filter(user=user).count() == 0

    def test_liked_item_cascade_delete_on_user_delete(self):
        user = baker.make(User)
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        LikedItem.objects.create(
            user=user,
            content_type=content_type,
            object_id=collection.id
        )

        user.delete()

        assert LikedItem.objects.count() == 0
