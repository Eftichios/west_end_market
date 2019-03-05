from django import forms
from django.contrib.auth.models import User
from west_end_market.models import Listing, Category
from django.utils import timezone


class ListingForm(forms.ModelForm):
    title = forms.CharField(required=True, max_length=100, help_text="Please enter the title of the Listing.")
    description = forms.CharField(max_length=250, help_text="Please enter the description of the Listing.")
    price = forms.IntegerField(required=True, help_text="Please enter the price of the Listing.")
    category = forms.ModelChoiceField(Category.objects.all(), required=True, help_text="Please enter the category of the Listing.")
    user = forms.ModelChoiceField(User.objects.all(), help_text="User")
    date = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now())
    picture = forms.ImageField(required=False, help_text="Please add a picture.")
    postcode = forms.CharField(required=False, max_length=10, help_text="Please enter your Postcode")

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith("http://"):
            url = 'http://'+url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        model = Listing
        exclude = ()


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

