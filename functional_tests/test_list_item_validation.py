from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    """
    Tests that we complain if we are given invlaid list items
    """
    def test_cannot_add_empty_list_item(self):
        # Edith goes to the home page and accidentally tries to submit an empty
        # list item: she hits <Enter> on an empty text box.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        # The home page refreshes, there is an error message saying that list
        # items cannot be blank.
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # Edith tries again, this time providing text for the item.
        # This now works.
        self.browser.find_element_by_id('id_new_item').send_keys('But milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # Somewhat perversely, she decides to try to submit a second blank item
        # and recieves a similar warning on the list page.
        self.browser.find_element_by_id('id_new_item').send_keys('\n')
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And Edith can correct things buyu filling some text in.
        self.browser.find_element_by_id('id_new_item').send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        self.fail('test not yet written')
