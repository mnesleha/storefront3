import pytest
from model_bakery import baker
from tags.models import TaggedItemManager, Tag, TaggedItem
from store.models import Product, Collection
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db
class TestTaggedItemManager:

    def test_get_tags_for_returns_queryset(self):
        collection = baker.make(Collection)
        result = TaggedItem.objects.get_tags_for(Collection, collection.id)

        assert hasattr(result, 'count')
        assert hasattr(result, 'filter')

    def test_get_tags_for_with_no_tags_returns_empty(self):
        collection = baker.make(Collection)
        result = TaggedItem.objects.get_tags_for(Collection, collection.id)

        assert result.count() == 0

    def test_get_tags_for_filters_by_object_type(self):
        collection = baker.make(Collection)
        product = baker.make(Product, collection=collection)
        tag = baker.make(Tag, label='test-tag')

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
        assert collection_tags.first().content_type == collection_ct
        assert product_tags.first().content_type == product_ct

    def test_get_tags_for_selects_related_tag(self):
        collection = baker.make(Collection)
        tag = baker.make(Tag, label='optimized-tag')
        content_type = ContentType.objects.get_for_model(Collection)

        TaggedItem.objects.create(
            tag=tag, content_type=content_type, object_id=collection.id)

        # This should not cause additional queries due to select_related
        tagged_items = TaggedItem.objects.get_tags_for(
            Collection, collection.id)
        tagged_item = tagged_items.first()

        # Access tag without additional query
        assert tagged_item.tag.label == 'optimized-tag'

    def test_manager_is_assigned_to_model(self):
        assert isinstance(TaggedItem.objects, TaggedItemManager)
