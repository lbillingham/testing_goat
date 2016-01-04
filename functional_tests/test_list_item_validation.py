from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    """
    Tests that we complain if we are given invlaid list items
    """
    def test_cannot_add_empty_list_item(self):
        # Edith goes to the home page and accidentally tries to submit an empty
        # list item: she hits <Enter> on an empty text box.
        self.browser.get(self.server_url)
        self.browser.find_elements_by_id('id_new_item').send_keys('\n')
        # The home page refreshes, there is an error message saying that list
        # items cannot be blank.
        error = self.browser.find_elements_by_css_selector('.has-error')
        self.asserEqual(error.text, "You can't have an empty list item")
        # Edith tries again, this time providing text for the item.
        # This now works.
        message = "I'm not nothing"
        self.browser.find_elements_by_id('id_new_item').send_keys(message)
        self.check_for_row_in_list_table('1: {}'.format(message))

        # Somewhat perversely, she decides to try to submit a second blank item
        # and recieves a similar warning on the list page.
        self.browser.find_elements_by_id('id_new_item').send_keys('\n')
        self.asserEqual(error.text, "You can't have an empty list item")

        # And Edith can correct things by filling some text in.
        second_message = "I'm not nothing neither"
        self.browser.find_elements_by_id('id_new_item').send_keys(second_message)
        self.check_for_row_in_list_table('1: {}'.format(message))
        self.check_for_row_in_list_table('1: {}'.format(second_message))
