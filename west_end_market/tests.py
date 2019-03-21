from django.test import TestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import os, socket

from django.utils import timezone

from django.core.urlresolvers import reverse

from west_end_market.setuptests import populate, add_category, add_listing, add_comment

from west_end_market.forms import ListingForm, UserForm
from west_end_market.models import Listing, User


def login(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    login = self.client.login(username='testuser', password='12345')



class IndexViewTests(TestCase):

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


##    def test_index_displays_newest_listings(self):
##        populate()
##
##        response = self.client.get(reverse('index'))
##
##        self.assertIn("CHECK FOR EACH OF THE NEWEST LISTINGS*".lower(), response.content.decode('ascii'))


##    def test_add_listing_form_is_displayed_correctly(self):
##        # Access the add_listing page
##        response = self.client.get(reverse('add_listing'))
##        
##        # Check that the form in the response context is an instance of ListingForm
##        self.assertTrue(isinstance(response.context['form'], ListingForm))
##        
##        # Check that the form is being displayed correctly
##        # Header
##        self.assertTrue('<h3>Create a Listing</h3>'.lower(), response.content.decode('ascii').lower())
##
##        #Buttons
##        self.assertTrue('type="submit" value="submit" >Create'.lower(), response.content.decode('ascii').lower())
##        self.assertTrue('type="submit" value="submit" disabled>Update'.lower(), response.content.decode('ascii').lower())


##    def test_logged_in_users_can_add_listings(self):
##        login()
##        # go to add listing page
##        # fill out form?


##    def test_users_not_logged_in_can_not_add_listings(self):
##        populate()
##        url = self.live_server_url
##        url = url.replace('localhost', '127.0.0.1')
##        self.browser.get(url + reverse('add_listing'))
##        self.assertEquals(self.browser.current_url, reverse('user_login'))
##        #self.assertIn('Only user that are logged in can add listings'.lower(), response.content.decode('ascii').lower())


##    def test_logged_in_users_can_add_comments(self):
##        populate()
##        login()
##        # go to a listing page
##        # fill out comment form and submit
##        # check that the information we just submitted can be found on the listing page


##    def test_users_not_logged_in_can_not_add_comments(self):
##        populate()
##        # log in
##        # go to a listing page
##        # fill out comment form and submit
##        # check that the information we just submitted can be found on the listing page


    def test_username_is_displayed_on_index_when_logged_in(self):
        login(self)
        response = self.client.get(reverse('index'))
        self.assertIn('Welcome, testuser!'.lower(), response.content.decode('ascii').lower())


    def test_guest_is_displayed_on_index_when_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertIn('Welcome!'.lower(), response.content.decode('ascii').lower())


    def test_message_when_looking_for_category_that_does_not_exist(self):
        populate()
        response = self.client.get(reverse('show_category', args=['notacategory']))
        self.assertIn("There is no such category. Please check the url and try again!".lower(), response.content.decode('ascii').lower())


##    def test_message_when_category_has_no_listings(self):
##        populate()
##        response = self.client.get(reverse('category', args=['school']))
##        self.assertIn("Category has no listings".lower(), response.content.decode('ascii').lower())


##    def test_message_when_looking_for_listing_that_does_not_exist(self):
##        populate()
##        response = self.client.get(reverse('show_listing', args=['999']))
##        self.assertIn("Listing does not exist".lower(), response.content.decode('ascii').lower())


    def test_message_when_looking_for_user_that_does_not_exist(self):
        populate()
        response = self.client.get(reverse('user_profile', args=['notauser']))
        self.assertIn("There is no such user. Please check the url and try again!".lower(), response.content.decode('ascii').lower())


    def test_message_when_user_has_no_listings(self):
        populate()
        response = self.client.get(reverse('user_profile', args=['userNoListings']))
        self.assertIn("This user currently has no listings!".lower(), response.content.decode('ascii').lower())


    def test_user_can_view_all_listings_from_a_single_user(self):
        #
        populate()

        # Retrieve categories and pages from database
        user = User.objects.get(username='JohnPope')
        userlistings = Listing.objects.filter(user=user)

        response = self.client.get(reverse('user_profile', args=['JohnPope']))

        # Check context dictionary filled
        self.assertCountEqual(response.context['listings'], userlistings)


##    def test_message_when_search_has_no_results(self):
        
        


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


