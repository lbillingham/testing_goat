from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    """
    Tests that we complain if we are given invlaid list items
    """
    def test_cannot_add_empty_list_item(self):
        # Edith goes to the home page and accidentally tries to submit an empty
        # list item: she hits <Enter> on an empty text box.
        #
        # The home page refreshes, there is an error message saying that list
        # items cannot be blank.
        #
        # Edith tries again, this time providing text for the item.
        # This now works.
        #
        # Somewhat perversely, she decides to try to submit a second blank item
        # and recieves a similar warning on the list page.
        #
        # And Edith can correct things buyu filling some text in.
        self.fail('test not yet written')
