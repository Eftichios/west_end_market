from django import forms
from django.contrib.auth.models import User
from west_end_market.models import Listing, Category, UserProfile, Comment


class ListingForm(forms.ModelForm):
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


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)
