from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from west_end_market.models import Category, Listing
from west_end_market.forms import ListingForm
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    return render(request,'west_end_market/index.html', {})


def add_listing(request):
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            print("FORM SAVED!!!")
            return index(request)
    else:
        print(form.errors)

    return render(request, 'west_end_market/add_listing.html', {'form': form})
