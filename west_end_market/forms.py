from django import forms
from django.contrib.auth.models import User
from west_end_market.models import Listing, Category, UserProfile
from django.utils import timezone


class ListingForm(forms.ModelForm):
    # title = forms.CharField(max_length=100, help_text="Please enter the title of the Listing.")
    # description = forms.CharField(max_length=250, help_text="Please enter the description of the Listing.")
    # price = forms.IntegerField(help_text="Please enter the price of the Listing.", default=0)
    # picture = forms.ImageField(help_text="Please add a picture.")
    # postcode = forms.CharField(max_length=10, help_text="Please enter your Postcode")
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith("http://"):
            url = 'http://'+url
            cleaned_data['url'] = url

            return cleaned_data

    class Meta:
        model = Listing
        exclude = ('user', 'date')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
