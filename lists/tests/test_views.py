from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm
from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):

    maxDiff = None
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
            )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_displays_only_itms_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='ooo item 1', list=correct_list)
        Item.objects.create(text='two-thy item', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/{0:d}/'.format(correct_list.id))

        self.assertContains(response, 'ooo item 1')
        self.assertContains(response, 'two-thy item')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
            )
        self.assertEqual(response.status_code, 302)
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{0:d}/'.format(new_list.id))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new' , data={'item_text':''})
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_are_not_saved(self):
        self.client.post('lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{0:d}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='ooo item 1', list=list_)
        Item.objects.create(text='two-thy item', list=list_)

        response = self.client.get('/lists/{0:d}/'.format(list_.id))

        self.assertContains(response, 'ooo item 1')
        self.assertContains(response, 'two-thy item')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{0:d}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/{0:d}/'.format(correct_list.id),
                data={'item_text': 'A new item for an existing list'}
                )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                '/lists/{0:d}/'.format(correct_list.id),
                data={'item_text': 'A new item for an existing list'}
                )

        self.assertRedirects(response, '/lists/{0:d}/'.format(correct_list.id))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            '/lists/{0:d}/'.format(list_.id),
            data={'item_text':''}
            )
        self.assertEqual(response.status_code, 200) # OK
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
