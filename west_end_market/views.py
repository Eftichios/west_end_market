from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from west_end_market.models import Category, Listing, User, Comment
from west_end_market.forms import ListingForm, UserForm, UserProfileForm, CommentForm
from django.contrib.auth.decorators import login_required


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
            listing.user = User.objects.get(username='Maria')
            setattr(listing.category, 'listings', listing.category.listings+1)
            listing.id = listing.category[0:1] + str(listing.category.listings)
            listing.category.save()
            listing.date = timezone.now()
            listing.save()
            return index(request)
    else:
        print(form.errors)

    return render(request, 'west_end_market/add_listing.html', {'form': form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'west_end_market/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your West End Market account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'west_end_market/loginpage.html', {})



@login_required
def user_logout(request):
    login(request)
    return HttpResponseRedirect(reverse('index'))


"""
def my_listings(request):
    return render(request, 'west_end_market/mylistings.html', {})
"""


def show_listing(request, listing_id):
    context_dict = {}
    try:
        listing = Listing.objects.get(id=listing_id)
        comments = Comment.objects.filter(listing=listing)
        context_dict['comments'] = comments
        context_dict['listing'] = listing
        # if user is logged in then they can comment
        if request.method == "POST":
            try:
                listing = Listing.objects.get(id=listing_id)
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.listing = listing
                    comment.user = request.user
                    comment.save()
                    return HttpResponseRedirect(reverse('show_listing', args=(listing_id,)))
            except Listing.DoesNotExist:
                form = None
        else:
            form = CommentForm()
    except Listing.DoesNotExist:
        context_dict['listing'] = None
        context_dict['comments'] = None
    context_dict["form"] = form
    return render(request, 'west_end_market/listing.html', context_dict)


def user_profile(request, username):
    context_dict = {}
    try:
        user = User.objects.get(username=username)
        listings = Listing.objects.filter(user=user)
        context_dict['listings'] = listings
        context_dict['user'] = user
    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['listings'] = None
    return render(request, 'west_end_market/user_profile.html', context_dict)


