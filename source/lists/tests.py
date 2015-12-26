from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


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


class NewItemTest(TestCase):

    def test_can_save_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
                '/lists/{0:d}/add_item'.format(correct_list.id),
                data={'item_text': 'A new item for an existing list'}
                )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                '/lists/{0:d}/add_item'.format(correct_list.id),
                data={'item_text': 'A new item for an existing list'}
                )

        self.assertRedirects(response, '/lists/{0:d}/'.format(correct_list.id))


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


class ListAndItemModelTests(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'the 1st (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'item numero 2'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_item.list, list_)

