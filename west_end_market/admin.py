from django.contrib import admin
from west_end_market.models import Category, Listing, Comment, UserProfile

# register the models
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(UserProfile)
