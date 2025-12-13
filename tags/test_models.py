import pytest
from model_bakery import baker
from django.contrib.contenttypes.models import ContentType
from tags.models import Tag, TaggedItem
from store.models import Product, Collection


@pytest.mark.django_db
class TestTagModel:

    def test_create_tag(self):
        tag = baker.make(Tag, label='electronics')

        assert tag.id is not None
        assert tag.label == 'electronics'

    def test_tag_string_representation(self):
        tag = baker.make(Tag, label='books')

        assert str(tag) == 'books'


@pytest.mark.django_db
class TestTaggedItemModel:

    def test_create_tagged_item(self):
        tag = baker.make(Tag, label='featured')
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        tagged_item = TaggedItem.objects.create(
            tag=tag,
            content_type=content_type,
            object_id=collection.id
        )

        assert tagged_item.id is not None
        assert tagged_item.tag == tag
        assert tagged_item.content_object == collection

    def test_get_tags_for_product(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        tag1 = baker.make(Tag, label='new')
        tag2 = baker.make(Tag, label='sale')

        content_type = ContentType.objects.get_for_model(Product)
        TaggedItem.objects.create(
            tag=tag1, content_type=content_type, object_id=product.id)
        TaggedItem.objects.create(
            tag=tag2, content_type=content_type, object_id=product.id)

        tagged_items = TaggedItem.objects.get_tags_for(Product, product.id)

        assert tagged_items.count() == 2
        tags = [item.tag.label for item in tagged_items]
        assert 'new' in tags
        assert 'sale' in tags

    def test_get_tags_for_collection(self):
        collection = baker.make(Collection)
        tag1 = baker.make(Tag, label='featured')
        tag2 = baker.make(Tag, label='trending')

        content_type = ContentType.objects.get_for_model(Collection)
        TaggedItem.objects.create(
            tag=tag1, content_type=content_type, object_id=collection.id)
        TaggedItem.objects.create(
            tag=tag2, content_type=content_type, object_id=collection.id)

        tagged_items = TaggedItem.objects.get_tags_for(
            Collection, collection.id)

        assert tagged_items.count() == 2

    def test_tagged_item_with_generic_foreign_key(self):
        tag = baker.make(Tag, label='important')
        collection = baker.make(Collection)
        content_type = ContentType.objects.get_for_model(Collection)

        tagged_item = TaggedItem.objects.create(
            tag=tag,
            content_type=content_type,
            object_id=collection.id
        )

        assert tagged_item.content_object == collection
        assert isinstance(tagged_item.content_object, Collection)

    def test_multiple_tags_for_same_object(self):
        collection = baker.make(Collection)
        tag1 = baker.make(Tag, label='tag1')
        tag2 = baker.make(Tag, label='tag2')
        tag3 = baker.make(Tag, label='tag3')

        content_type = ContentType.objects.get_for_model(Collection)

        TaggedItem.objects.create(
            tag=tag1, content_type=content_type, object_id=collection.id)
        TaggedItem.objects.create(
            tag=tag2, content_type=content_type, object_id=collection.id)
        TaggedItem.objects.create(
            tag=tag3, content_type=content_type, object_id=collection.id)

        tagged_items = TaggedItem.objects.get_tags_for(
            Collection, collection.id)

        assert tagged_items.count() == 3

    def test_tags_for_different_objects(self):
        tag = baker.make(Tag, label='shared-tag')
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)

        collection_ct = ContentType.objects.get_for_model(Collection)
        product_ct = ContentType.objects.get_for_model(Product)

        TaggedItem.objects.create(
            tag=tag, content_type=collection_ct, object_id=collection.id)
        TaggedItem.objects.create(
            tag=tag, content_type=product_ct, object_id=product.id)

        collection_tags = TaggedItem.objects.get_tags_for(
            Collection, collection.id)
        product_tags = TaggedItem.objects.get_tags_for(Product, product.id)

        assert collection_tags.count() == 1
        assert product_tags.count() == 1
