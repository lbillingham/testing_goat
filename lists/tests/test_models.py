from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List

class ItemModelTests(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_string_repr(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='1st item')
        item2 = Item.objects.create(list=list_, text='2nd item')
        item3 = Item.objects.create(list=list_, text='3rd item')
        in_expected_order = [item1, item2, item3]
        self.assertEqual(list(Item.objects.all()), in_expected_order)

    def test_cannot_add_empty_list_item(self):
        list_ =  List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_within_a_list_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='in-list dupe')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='in-list dupe')
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='cross list dupe')
        item2 = Item.objects.create(list=list2, text='cross list dupe')
        item1.full_clean() # shouldn't raise
        item2.full_clean() # shouldn't raise


class ListModelTests(TestCase):
    def test_can_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{:d}/'.format(list_.id))
