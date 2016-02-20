from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    """
    Minimal test to show that we are loading the css etc.
    """
    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 786)

        # she notices the box is nicely centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] /2.,
                512,
                delta=7
                )
        # She starts a new list and sees that the input is centered ther too
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] /2.,
                512,
                delta=7
                )
