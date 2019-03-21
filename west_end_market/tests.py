from django.test import TestCase

from django.core.urlresolvers import reverse

from west_end_market.forms import ListingForm, UserForm

# Helper functions - may move to sepearate file later

def create_listings():
    # List of listings
    listings = []

    # Create listings

    return listings


def create_user():

def create_comments():




class IndexViewTests(TestCase):

    def test_index_uses_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'west_end_market/index.html')
    
    def test_index_shows_newest_listings(self):
        # Access index with empty database
        response = self.client.get(reverse('index'))

        # Context dictionary is then empty
        self.assertCountEqual(response.context['listings'], [])

        listings = test_utils.create_listings()

        # Access index with database filled
        response = self.client.get(reverse('index'))

        # Retrieve categories and pages from database
        listings = Listing.objects.order_by('-date')[:8]

        # Check context dictionary filled
        self.assertCountEqual(response.context['listings'], listings)

        
    def test_index_displays_eight_newest_listings(self):
        # Create listings
        create_listings()

        # Access index
        response = self.client.get(reverse('index'))

    def test_add_listing_form_is_displayed_correctly(self):
        # Access the add_listing page
        response = self.client.get(reverse('add_listing'))
        
        # Check that the form in the response context is an instance of ListingForm
        self.assertTrue(isinstance(response.context['form'], ListingForm))
        
        # Check that the form is being displayed correctly
        # Header
        self.assertTrue('<h3>Create a Listing</h3>'.lower(), response.content.decode('ascii').lower())

        #Buttons
        self.assertTrue('type="submit" value="submit" >Create'.lower(), response.content.decode('ascii').lower())
        self.assertTrue('type="submit" value="submit" disabled>Update'.lower(), response.content.decode('ascii').lower())


    def test_logged_in_users_can_add_listings(self):
        # log in
        # go to add listing page
        # fill out form?

    def test_users_not_logged_in_can_not_add_listings(self):
        #
        response = self.client.get(reverse('add_listings'))
        self.assertIn('Only user that are logged in can add listings'.lower(), response.content.decode('ascii').lower())
        

    def test_listing_is_saved_correctly(self):

    def test_username_is_displayed_on_index_when_logged_in(self):
        # login
        response = self.client.get(reverse('index'))
        self.assertIn('Hello, [username]'.lower(), response.content.decode('ascii').lower())

    def test_guest_is_displayed_on_index_when_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertIn('Hello, Guest'.lower(), response.content.decode('ascii').lower())

    def test_message_when_looking_for_category_that_does_not_exist(self):
        # create categories
        response = self.client.get(reverse('category', args=['notacategory']))
        self.assertIn("Category has no listings".lower(), response.content.decode('ascii').lower())

    def test_message_when_category_has_no_listings(self):
        # create category with no listings
        response = self.client.get(reverse('category', args=['school']))
        self.assertIn("Category has no listings".lower(), response.content.decode('ascii').lower())

    def test_message_when_looking_for_listing_that_does_not_exist(self):
        response = self.client.get(reverse('listing', args=['999']))
        self.assertIn("Listing does not exist".lower(), response.content.decode('ascii').lower())

    def test_message_when_looking_for_user_that_does_not_exist(self):
        response = self.client.get(reverse('listing', args=['notauser']))
        self.assertIn("User does not exist".lower(), response.content.decode('ascii').lower())

    def test_message_when_user_has_no_listings(self):
        # create user with no listings
        response = self.client.get(reverse('user_profile', args=['testuser']))
        self.assertIn("User has no listings".lower(), response.content.decode('ascii').lower())
        


#Tests to consider

#Pages use base template
#Check we can register and login correctly

#Add listings:
#Users can add new listings

#Category pages:
#Category is empty
#Category doesn't exist

#Listing pages:
#Listing doesn't exist

#User profiles:
#User doesn't exist


