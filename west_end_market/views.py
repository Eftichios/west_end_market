from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from west_end_market.models import Category, Listing, User, Comment, UserProfile
from west_end_market.forms import ListingForm, UserForm, UserProfileForm, CommentForm
from django.contrib.auth.decorators import login_required


def index(request):
    listings_list = Listing.objects.order_by('-date')[:8]
    context_dict = {'listings': listings_list}
    return render(request, 'west_end_market/index.html', context_dict)


@login_required
def add_listing(request):
    form = ListingForm()
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.picture = form.cleaned_data['picture']
            listing.user = request.user
            setattr(listing.category, 'listings', listing.category.listings+1)
            listing.id = listing.category.name[0:3] + str(listing.category.listings)
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
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.picture = profile_form.cleaned_data['picture']
            profile.save()
            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'west_end_market/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):

    # redirect logged-in users to the home page if they try to access the login page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    success = True
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
            success = False
            return render(request, 'west_end_market/loginpage.html', {"success": success})

    else:
        return render(request, 'west_end_market/loginpage.html', {"success": success})



@login_required
def user_logout(request):
    logout(request)
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
    context_dict["user"] = request.user
    return render(request, 'west_end_market/listing.html', context_dict)


def show_category(request, category_title):
    if category_title == 'all':
        return render(request, 'west_end_market/category_page.html', {'listings': Listing.objects.all(), 'category': 'all'})
    context_dict = {}
    try:
        category = Category.objects.get(name=category_title)
        listings = Listing.objects.filter(category=category)
        context_dict["category"] = category
        context_dict["listings"] = listings
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['listings'] = None
    return render(request, 'west_end_market/category_page.html', context_dict)


def user_profile(request, user_username):
    context_dict = {}
    try:
        user = User.objects.get(username=user_username)
        listings = Listing.objects.filter(user=user)
        context_dict['listings'] = listings
        context_dict['user'] = user
    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['listings'] = None
    return render(request, 'west_end_market/user_profile.html', context_dict)


def search_results(request):
    context_dict = {}
    listings = Listing.objects.all()
    results = []
    if request.method == 'POST':
        context_dict["search"] = request.POST.get("search")
        for listing in listings:
            if request.POST.get("search").lower() in listing.title.lower() or request.POST.get("search").lower() in listing.description.lower():
                results += [listing]
        context_dict["results"] = results
    else:
        context_dict["results"] = results
    return render(request, 'west_end_market/search_results.html', context_dict)


@login_required
def my_account(request):
    user = request.user
    listings = Listing.objects.filter(user=user)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'west_end_market/my_account.html', {'listings':listings, 'user': user, 'profile': profile})


@login_required
def edit_profile(request):
    edited = False
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        user.username = request.POST.get("username")
        user.set_password = request.POST.get("password")
        user.email = request.POST.get("email")
        if request.FILES.get("picture"):
            profile.picture = request.FILES.get("picture")
            profile.save()
        user.save()
        edited = True

    return render(request, 'west_end_market/edit_profile.html', {'user': user, 'profile': profile, 'edited': edited})


@login_required
def edit_listing(request, listing_id):
    edited = False
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST' and listing:
        listing.title = request.POST.get("title")
        listing.description = request.POST.get("description")
        listing.price = request.POST.get("price")
        if request.FILES.get("picture"):
            listing.picture = request.FILES.get("picture")
        listing.postcode = request.POST.get("postcode")
        listing.date = timezone.now()
        listing.save()
        edited = True

    return render(request, 'west_end_market/edit_listing.html', {"listing": listing, 'edited': edited})


def cookie_policy(request):
    return render(request, 'west_end_market/cookie_policy.html',{})
