from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    """
    Test our onboarding poorocess for new visitors to our sitre
    """
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()

    def test_can_start_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do list app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish writing the test')


        # She is invited to enter an to-do item straight away

        # She types "Buy peacock feathers" into a text box
        #   (Edith's hobby is tying fly-fishing lures)

        # When she hits <enter>, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a textbox inviting her to add anoter item
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees
        #  that it has generated a unique URL for her --- there is some
        #  explanetory text to that effect.

        # Edith visits her the unique URL she was given --- her list is still there

        # Satisfied, Edith goes back to sleep
if '__main__' == __name__:
    unittest.main()
