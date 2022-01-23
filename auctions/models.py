from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    photo_URL = models.URLField('Photo URL (optional)', blank=True, max_length=500)
    # Categories could be made as a separate class, but since we hard code all 
    # of them in advance, they can be added as a field in this class, too.
    CATEGORIES = [
        ("Books", "Books"), ("Fashion", "Fashion"), ("Home", "Home"),
        ("Tech", "Tech"), ("Tools", "Tools"), ("Other", "Other")]
    category = models.CharField('Category (optional)', max_length=10, blank=True, choices=CATEGORIES)
    status = models.CharField(max_length=1, default="A")
    watch = models.ManyToManyField(User, blank=True, related_name="watchlist")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Comments(models.Model):
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField("")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment[:10]}..."

class Bids(models.Model):
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField("",max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bid}"

