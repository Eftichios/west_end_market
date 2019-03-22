from django.shortcuts import render
from django.views.generic.edit import DeleteView
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from west_end_market.models import Category, Listing, User, Comment, UserProfile
from west_end_market.forms import ListingForm, UserForm, UserProfileForm, CommentForm
from django.contrib.auth.decorators import login_required


# view for the index page
def index(request):
    # get the 8 latest listings and pass them to the template
    listings_list = Listing.objects.order_by('-date')[:8]
    context_dict = {'listings': listings_list}
    return render(request, 'west_end_market/index.html', context_dict)


# logged in users should be able to create new listings
@login_required
def add_listing(request):
    form = ListingForm()
    context_dict={}
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            # create a listing with the attributes provided
            listing = form.save(commit=False)
            listing.picture = form.cleaned_data['picture']
            listing.user = request.user

            # increase the item count in the relevant category
            setattr(listing.category, 'listings', listing.category.listings+1)

            # id is the first 3 letters of the category and previous number plus 1
            listing.id = listing.category.name[0:3] + str(listing.category.listings)
            listing.category.save()
            listing.date = timezone.now()
            listing.save()
            return index(request)
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'west_end_market/add_listing.html', context_dict)


# guests should be able to create an account
def register(request):
    registered = False
    context_dict = {}
    if request.method == 'POST':
        # custom check to see if password is invalid
        if len(request.POST.get("password")) < 6 or (not request.POST.get("username").isalnum()):
            user_form = UserForm()
            profile_form = UserProfileForm()
            context_dict["user_form"] = user_form
            context_dict["profile_form"] = profile_form
            context_dict["registered"] = registered
            context_dict["password_short"] = len(request.POST.get("password")) < 6
            context_dict["invalid_username"] = (not request.POST.get("username").isalnum())
            return render(request, 'west_end_market/register.html', context_dict)
        # user form is username/email/password and profile form is the profile picture
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        # if both forms are valid, create a new user
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
    context_dict["user_form"] = user_form
    context_dict["profile_form"] = profile_form
    context_dict["registered"] = registered
    return render(request, 'west_end_market/register.html', context_dict)


# allows a registered user to log in
def user_login(request):
    context_dict = {}
    # redirect logged-in users to the home page if they try to access the login page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            success = False
            context_dict['success'] = False
            return render(request, 'west_end_market/loginpage.html', context_dict)

    else:
        context_dict['success'] = True
        return render(request, 'west_end_market/loginpage.html', context_dict)


# logs out a logged in user
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# displays the listings with id = listing_id
def show_listing(request, listing_id):
    context_dict = {}
    try:
        # get the listing and its comments if they exist
        listing = Listing.objects.get(id=listing_id)
        comments = Comment.objects.filter(listing=listing)
        context_dict['comments'] = comments
        context_dict['listing'] = listing

        # if user is logged in then they can see the form for comments
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
        form = None
    context_dict["form"] = form
    context_dict["user"] = request.user
    return render(request, 'west_end_market/listing.html', context_dict)


# shows the listings in a category, uses sort_by to enable sorting functionality, default is sorted by date
def show_category(request, category_title, sort_by='date'):
    context_dict = {}
    # show all available listings if title is 'all'
    if category_title == 'all':
        context_dict["category"] = 'all'
        context_dict["listings"] = Listing.objects.all()
        context_dict["category_name"] = 'all'
        context_dict["sort_by"] = sort_by
        return render(request, 'west_end_market/category_page.html', context_dict)
    try:
        # get the category and its listings
        category = Category.objects.get(name=category_title)
        listings = Listing.objects.filter(category=category)
        context_dict["category"] = category
        context_dict["listings"] = listings
        context_dict["category_name"] = category_title
        context_dict["sort_by"] = sort_by
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['listings'] = None
    return render(request, 'west_end_market/category_page.html', context_dict)


# displays the profile of the user and their listings
def user_profile(request, user_username):
    context_dict = {}
    try:
        # get the user and their profile if query was correct, otherwise return None
        user = User.objects.get(username=user_username)
        profile = UserProfile.objects.get(user=user)
        listings = Listing.objects.filter(user=user)
        context_dict['listings'] = listings
        context_dict['user'] = user
        context_dict['profile'] = profile
    except User.DoesNotExist:
        context_dict['profile'] = None
        context_dict['user'] = None
        context_dict['listings'] = None
    return render(request, 'west_end_market/user_profile.html', context_dict)


# searches for listings based on a query, uses sort_by to enable sorting functionality, default is sorted by date
def search_results(request, search=None, sort_by='date'):
    context_dict = {}
    listings = Listing.objects.all()
    results = []
    if request.method == 'POST':
        search = request.POST.get("search")
    if search == "" or search == "all" or (not search):
        search = "all"
        results = listings
    else:
        for listing in listings:
            if search.lower() in listing.title.lower() or search.lower() in listing.description.lower():
                    results += [listing]
    context_dict["results"] = results
    context_dict["sort_by"] = sort_by
    context_dict["search"] = search
    return render(request, 'west_end_market/search_results.html', context_dict)


# displays logged in users account
@login_required
def my_account(request):
    user = request.user
    listings = Listing.objects.filter(user=user)
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    context_dict = {'listings': listings, 'user': user, 'profile': profile}
    return render(request, 'west_end_market/my_account.html', context_dict)


# allows users to edit profile
@login_required
def edit_profile(request):
    edited = False
    user = request.user
    # retreive the user's profile, some users like superusers dont have a profile
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        # check that the password is valid
        if len(request.POST.get("password")) < 6:
            context_dict = {'user': user, 'profile': profile, 'edited': edited, 'password_short': True}
            return render(request, 'west_end_market/edit_profile.html', context_dict)
        # update the user's details and its profile
        user.username = request.POST.get("username")
        user.set_password(request.POST.get("password"))
        user.email = request.POST.get("email")
        if request.FILES.get("picture") and profile:
            profile.picture = request.FILES.get("picture")
            profile.save()
        user.save()
        edited = True
    context_dict = {'user': user, 'profile': profile, 'edited': edited}
    return render(request, 'west_end_market/edit_profile.html', context_dict)


# allow users to edit their own listings
@login_required
def edit_listing(request, listing_id):
    edited = False
    # get the listing with listing_id
    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        listing = None
    user = request.user
    if request.method == 'POST' and listing:
        # update listing's details
        listing.title = request.POST.get("title")
        listing.description = request.POST.get("description")
        listing.price = request.POST.get("price")
        if request.FILES.get("picture"):
            listing.picture = request.FILES.get("picture")
        listing.postcode = request.POST.get("postcode")
        listing.date = timezone.now()
        listing.save()
        edited = True

    context_dict = {"listing": listing, 'edited': edited, 'user': user}
    return render(request, 'west_end_market/edit_listing.html', context_dict)


# allows a user to delete their own listings
class ListingDelete(DeleteView):
    model = Listing
    success_url = reverse_lazy('index')
    template_name = 'west_end_market/delete_listing.html'

    # passes in which user is logged in so a validation can be made in the template
    def get_context_data(self, **kwargs):
        context = super(ListingDelete, self).get_context_data(**kwargs)
        context.update({'user': self.request.user})
        return context


# view for the cookie page
def cookie_policy(request):
    return render(request, 'west_end_market/cookie_policy.html', {})
