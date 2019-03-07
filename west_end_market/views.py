from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from west_end_market.models import Listing
from west_end_market.models import Category as C, Listing as L, User as U
from west_end_market.forms import ListingForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    listings_list = Listing.objects.order_by('-date')[:8]
    context_dict = {'listings': listings_list}
    return render(request, 'west_end_market/index.html', context_dict)


def add_listing(request):
    form = ListingForm()
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.picture = form.cleaned_data['picture']
            listing.user = U.objects.get(username='Maria')
            setattr(listing.category, 'listings', listing.category.listings+1)
            listing.category.save()
            listing.date = timezone.now()
            listing.save()
            return index(request)
    else:
        print(form.errors)

    return render(request, 'west_end_market/add_listing.html', {'form': form})


"""
def register(request):
    return render(request, 'west_end_market/register.html', {})
"""


def user_login(request):
    return render(request,'west_end_market/loginpage.html', {})


"""
@login_required
def user_logout(request):
    login(request)
    return HttpResponseRedirect(reverse('index'))
"""


"""
@login_required
def my_listings(request):
    return render(request, 'west_end_market/mylistings.html', {})
"""


"""
def show_listing(request, listing_id):
    context_dict = {}
    try:
        listing = Listing.objects.get(listing_id=listing_id)
        comments = Comment.onjects.filter(listing=listing)
        context_dict['comments'] = comments
        context_dict['listing'] = listing
    except Listing.DoesNotExist:
        context_dict['listing'] = None
        context_dict['comments'] = None
    return render(request,'rango/listing.html', context_dict)
"""


def user_profile(request):
    return render(request, 'west_end_market/user_profile.html', {})
