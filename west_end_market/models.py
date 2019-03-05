from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):

    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    listings = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(null=True)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing)

    def __str__(self):
        return self.comment