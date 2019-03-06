from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from west_end_market.models import Category as C, Listing as L, User as U
from west_end_market.forms import ListingForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    return render(request, 'west_end_market/index.html', {})


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
