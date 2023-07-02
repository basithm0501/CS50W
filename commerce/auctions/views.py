from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all(),
        "message": f"{len(Listing.objects.all())} listing(s) found."
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        if request.POST["title"] is None:
            return render(request, "auctions/create.html", {
                "message": "Must have a title!"
            })
        if len(request.POST["title"]) > 32:
            return render(request, "auctions/create.html", {
                "message": "Title must be less than 32 characters!"
            })
        if request.POST["starting_bid"] is None:
            return render(request, "auctions/create.html", {
                "message": "Starting bid is invalid!"
            })
        listing = Listing(title=request.POST["title"], 
                          description=request.POST["description"],
                          user=request.user,
                          image=request.POST["image"],
                          category=request.POST["category"])
        listing.save()
        start_bid = Bid(value=request.POST["starting_bid"],
                        user=request.user,
                        listing=listing)
        start_bid.save()
        listing.starting_bid = start_bid.value
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:  
        return render(request, "auctions/create.html")
    
def listing_page(request, listing_id):
    message = None
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        if (request.POST["bid"]) == "END":
            listing.closed = True
            listing.save()
        elif (request.POST["bid"]) == "WL":
            listing.watching.add(request.user)
            listing.save()
        elif (request.POST["bid"]) == "-WL":
            listing.watching.remove(request.user)
            listing.save()
        else:
            try:
                float(request.POST["bid"])
            except ValueError:
                if request.POST["bid"] == "":
                    message = "You cannot make an empty comment."
                else:
                    new_comment = Comment(content=request.POST["bid"],
                            user=request.user,
                            listing=listing)
                    new_comment.save()
            else:
                if (float(request.POST["bid"]) > max_bid(listing)) and (float(request.POST["bid"]) > listing.starting_bid):
                    new_bid = Bid(value=request.POST["bid"],
                            user=request.user,
                            listing=listing)
                    new_bid.save()
                    listing.highest_bid = new_bid.value
                    listing.save()
                else:
                    message = "You must bid higher than the current bid."
    listing = Listing.objects.get(id=listing_id)
    category = None
    for c in CATEGORIES:
        if c[0] == listing.category:
            category = c[1]
            break
    users = []
    for bid in listing.bids.all():
        users.append(bid.user)
    high = users[-1]
    arebidder = request.user == high
    if request.user.is_authenticated:
        wlisted = listing in request.user.watchlist.all()
    else:
        wlisted = None
    return render(request, "auctions/page.html",{
        "listing": listing,
        "category": category,
        "num_bids": len(listing.bids.all())-1,
        "arebidder": arebidder,
        "high": high,
        "wlisted": wlisted,
        "comments": listing.comments.all(),
        "message": message
    })

def categories(request, code=None):
    if code==None:
        return render(request, "auctions/categories.html",{
            "codes": CATEGORIES,
        })
    else:
        return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(category=code).all(),
        "message": f"{len(Listing.objects.filter(category=code).all())} listing(s) found."
    })

def max_bid(l):
    vals = []
    for bid in l.bids.all():
        vals.append(bid.value)
    return max(vals)

def watch(request):
    return render(request, "auctions/index.html",{
        "listings": request.user.watchlist.all(),
        "message": f"{len(request.user.watchlist.all())} listing(s) in your watchlist."
    })