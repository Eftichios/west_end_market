from django.test import TestCase
from django.test import SimpleTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
import os, socket
from django.utils import timezone
from django.core.urlresolvers import reverse
from west_end_market.setuptests import populate, add_category, add_listing, add_comment
from west_end_market.forms import ListingForm, UserForm
from west_end_market.models import Listing, User, Category
from django.core.files.uploadedfile import SimpleUploadedFile

# Used to create a dummy user
def login(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    login = self.client.login(username='testuser', password='12345')



class DjangoTests(TestCase):

    def test_index_uses_template(self):
        # Access the index page
        response = self.client.get(reverse('index'))

        # Checks that index is using the correct template
        self.assertTemplateUsed(response, 'west_end_market/index.html')

        # Also checks that the index is using the base template, as the header implements this
        self.assertTemplateUsed(response, 'west_end_market/base.html')

    
    def test_index_content(self):
        # Access index with empty database
        response = self.client.get(reverse('index'))

        # Context dictionary is then empty
        self.assertCountEqual(response.context['listings'], [])

        #listings = create_listings()
        populate()

        # Access index with database filled
        response = self.client.get(reverse('index'))

        # Retrieve categories and pages from database
        listings = Listing.objects.order_by('-date')[:8]

        # Check context dictionary filled
        self.assertCountEqual(response.context['listings'], listings)


    def test_index_displays_newest_listings(self):
        # Populates the database with information
        populate()
        # Access the index page
        response = self.client.get(reverse('index'))
        # Gets the 8 newest listings
        listings = Listing.objects.order_by('-date')[:8]

        # Goes through the 8 newest listings and checks that their id can be found on the index page
        for l in listings:
            listing_id = l.id
            self.assertIn(listing_id.lower(), response.content.decode('ascii'))


    def test_add_listing_form_is_displayed_correctly(self):
        login(self)
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
        

    def test_users_not_logged_in_are_redirected_to_login_when_adding_listings(self):
        # Populates the database with information
        populate()
        # Access the add listing page
        response = self.client.get(reverse('add_listing'))
        # Checks that since the user is not logged in, they are redirected to the login page
        SimpleTestCase().assertRedirects(response, '/west_end_market/login/?next=/west_end_market/add_listing/')


    def test_logged_in_users_have_access_to_adding_comments(self):
        # Populates the database with information
        populate()
        # Logs into the website with a dummy account
        login(self)
        # Access the listing page of sch1
        response = self.client.get(reverse('show_listing', args=['sch1']))
        # Checks that the form used to add comments is present
        self.assertIn('form method="POST" class="post-form"'.lower(), response.content.decode('utf-8').lower())


    def test_users_not_logged_in_can_not_add_comments(self):
        # Populates the database with information
        populate()
        # Access the listing page of sch1
        response = self.client.get(reverse('show_listing', args=['sch1']))
        # Checks that the form used to add comments is not present, as the user is not logged in
        self.assertNotIn('form method="POST" class="post-form"'.lower(), response.content.decode('utf-8').lower())


    def test_username_is_displayed_on_index_when_logged_in(self):
        # Logs into the website with a dummy account
        login(self)
        # Access the index page
        response = self.client.get(reverse('index'))
        # Checks that the welcome message includes the name of the dummy account
        self.assertIn('Welcome, testuser!'.lower(), response.content.decode('ascii').lower())


    def test_guest_is_displayed_on_index_when_not_logged_in(self):
        # Access the index page
        response = self.client.get(reverse('index'))
        # Checks that the welcome message used is the standard one
        self.assertIn('Welcome!'.lower(), response.content.decode('ascii').lower())


    def test_message_when_looking_for_category_that_does_not_exist(self):
        # Populates the database with information
        populate()
        # Tries to access the page of a category that doesn't exist
        response = self.client.get(reverse('show_category', args=['notacategory']))
        # Checks that the appropriate error message is displayed
        self.assertIn("There is no such category. Please check the url and try again!".lower(), response.content.decode('ascii').lower())


    def test_message_when_category_has_no_listings(self):
        # Populates the database with information
        populate()
        # Access the page of the Other category, which when created in population() has no listings
        response = self.client.get(reverse('show_category', args=['other']))
        # Checks that the appropriate error message is displayed
        self.assertIn("This category currently has no listings!".lower(), response.content.decode('ascii').lower())


    def test_message_when_looking_for_listing_that_does_not_exist(self):
        # Populates the database with information
        populate()
        # Tries to access the page of a listing that doesn't exist
        response = self.client.get(reverse('show_listing', args=['999']))
        # Checks that the appropriate error message is displayed
        self.assertIn("There is no such listing. Please check the url and try again!".lower(), response.content.decode('ascii').lower())


    def test_message_when_looking_for_user_that_does_not_exist(self):
        # Populates the database with information
        populate()
        # Tries to access the page of a user that doesn't exist
        response = self.client.get(reverse('user_profile', args=['notauser']))
        # Checks that the appropriate error message is displayed
        self.assertIn("There is no such user. Please check the url and try again!".lower(), response.content.decode('ascii').lower())


    def test_message_when_user_has_no_listings(self):
        # Populates the database with information
        populate()
        # Access the page of the user userNoListings, which when created in population() has no listings
        response = self.client.get(reverse('user_profile', args=['userNoListings']))
        # Checks that the appropriate error message is displayed
        self.assertIn("This user currently has no listings!".lower(), response.content.decode('ascii').lower())


    def test_user_can_view_all_listings_from_a_single_user(self):
        # Populates the database with information
        populate()

        # Retrieve the listings of user JohnPope
        user = User.objects.get(username='JohnPope')
        userlistings = Listing.objects.filter(user=user)

        # Access the user profile page of JohnPope
        response = self.client.get(reverse('user_profile', args=['JohnPope']))

        # Check context dictionary filled
        self.assertCountEqual(response.context['listings'], userlistings)


##    def test_listing_form(self):
##        # Creates a listing form with data
##        form = ListingForm(data={"id": "sch4",
##                                 "title": "Maths For Dummies Brand New",
##                                 "description": "Selling for what I paid for it",
##                                 "price": 40,
##                                 "category": Category(name="school"),
##                                 "user": "JohnPope",
##                                 "date": timezone.now(),
##                                 "picture": '/testimage.png',
##                                 "postcode": "PC SCH1"})
##
##        print(form.errors)
##
##        # Checks that this form is valid
##        self.assertTrue(form.is_valid())


    def test_user_form(self):
        # Creates a user form with data
        form = UserForm(data={"username": "Jack",
                              "email": "Jack@email.com",
                              "picture":"Jack/profile.jpg",
                              "password": 'jackspassword'})

        # Checks that this form is valid
        self.assertTrue(form.is_valid())



