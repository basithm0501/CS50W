from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = [
        ("ATC", "Arts & Crafts"),
        ("ATM", "Automotive"),
        ("BAB", "Baby"),
        ("BPC", "Beauty & Personal Care"),
        ("BOK", "Books"),
        ("CMP", "Computers"),
        ("ELE", "Electronics"),
        ("WMN", "Women's Fashion"),
        ("MEN", "Men's Fashion"),
        ("GRL", "Girls' Fashion"),
        ("BOY", "Boys' Fashion"),
        ("HNH", "Health & Household"),
        ("HNK", "Home & Kitchen"),
        ("INS", "Industrial & Scientific"),
        ("LGG", "Luggage"),
        ("MNT", "Movies & Television"),
        ("MCV", "Music, CDs & Vinyl"),
        ("PSS", "Pet Supplies"),
        ("SFW", "Software"),
        ("SNO", "Sports & Outdoors"),
        ("THI", "Tools & Home Improvement"),
        ("TNG", "Toys & Games"),
        ("VDG", "Video Games"),
    ]

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name="listings")
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    starting_bid = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    highest_bid = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=3, choices=CATEGORIES, blank=True)
    closed = models.BooleanField(default=False)
    watching = models.ManyToManyField(User,blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    value = models.DecimalField(max_digits=20, decimal_places=2)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name="bids")
    listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"${self.value} Bid on {self.listing} by {self.user}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name="comments")
    listing = models.ForeignKey(Listing, blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"Comment on {self.listing} by {self.user}"