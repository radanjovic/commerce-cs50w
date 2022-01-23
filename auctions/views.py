from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def index(request):
    """Displays all listings to both logged in and logged out users"""
    listings = Listings.objects.filter(status="A").order_by("-created").all()
    # If we had highest bid in our listings model this would be easier, but it
    # works the same just like this too:
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, "auctions/index.html", {"listings":listings, "bids":bids})

def books(request):
    listings = Listings.objects.filter(status="A", category="Books").order_by("-created").all()
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, 'auctions/books.html', {"listings":listings, "bids":bids})

def fashion(request):
    listings = Listings.objects.filter(status="A", category="Fashion").order_by("-created").all()
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, 'auctions/fashion.html', {"listings":listings, "bids":bids})

def home(request):
    listings = Listings.objects.filter(status="A", category="Home").order_by("-created").all()
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, 'auctions/home.html', {"listings":listings, "bids":bids})

def tech(request):
    listings = Listings.objects.filter(status="A", category="Tech").order_by("-created").all()
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, 'auctions/tech.html', {"listings":listings, "bids":bids})

def tools(request):
    listings = Listings.objects.filter(status="A", category="Tools").order_by("-created").all()
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, 'auctions/tools.html', {"listings":listings, "bids":bids})

def other(request):
    listings = Listings.objects.filter(status="A", category="Other").order_by("-created").all()
    bid = {}
    bids = []
    for listing in listings:
        highest_bid = Bids.objects.filter(listing_id=listing.id).order_by("-bid").first()
        if highest_bid:
            bid["id"] = listing.id
            bid["bid"] = highest_bid.bid
            bids.append(bid)
            bid = {}
        else:
            bid["id"] = listing.id
            bid["bid"] = listing.initial_price
            bids.append(bid)
            bid = {}
    return render(request, 'auctions/other.html', {"listings":listings, "bids":bids})


def listing(request, listing_id):
    """ Displays one particular listing, by its ID with options to bid, watchlist or comment for logged in users"""
    try:
        form_c = CommentForm()
        form_b = BidForm()
        highest_bid = Bids.objects.filter(listing_id=listing_id).order_by("-bid").first()
        initial_price = Listings.objects.get(id=listing_id).initial_price
        listing = Listings.objects.get(id=listing_id)
        comments = Comments.objects.filter(listing_id=listing_id).all()
    
        if request.method == "POST":
            # Closing auction
            if "close" in request.POST:
                if listing.owner == request.user:
                    listing.status = "C"
                    listing.save()
                    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
                
            elif "watchlist" in request.POST:
                # Adding or removing listing from watchlist
                watchlist = request.user.watchlist
                if listing in watchlist.all():
                    watchlist.remove(listing)
                    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
                else:
                    watchlist.add(listing)
                    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

            elif "post_comment" in request.POST:
                # Comments on listings
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.user_id = request.user
                    comment.listing_id = Listings.objects.get(id=listing_id)
                    comment.save()
                    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
                
                
            elif "post_bid" in request.POST:
                # Bidding on listings
                if highest_bid:
                    form = BidForm(request.POST)
                    if form.is_valid():
                        bid = form.save(commit=False)
                        if bid.bid > highest_bid.bid:
                            bid.user_id = request.user
                            bid.listing_id = Listings.objects.get(id=listing_id)
                            bid.save()
                            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
                        else:
                            return render(request, 'auctions/listing.html', {
                                "listing":listing, "comments":comments, "form_c":form_c, 
                                "form_b":form_b, "bid":highest_bid, "message":"Bid must be higher than highest bid!"
                                })
                    
                else:
                    form = BidForm(request.POST)
                    if form.is_valid():
                        bid = form.save(commit=False)
                        if bid.bid > initial_price:
                            bid.user_id = request.user
                            bid.listing_id = Listings.objects.get(id=listing_id)
                            bid.save()
                            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
                        else:
                            return render(request, 'auctions/listing.html', {
                                "listing":listing, "comments":comments, "form_c":form_c, 
                                "form_b":form_b, "bid":highest_bid, "message":"Bid must be higher than initial price!"
                                })                        
        
        return render(request, 'auctions/listing.html', {
            "listing":listing, "comments":comments, "form_c":form_c, "form_b":form_b, "bid":highest_bid,
            })
            
    except:
        HttpResponse("No such entry.")


@login_required
def watchlist(request):
    """Displays all watchlisted listings for logged in user"""
    watch_list = request.user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        "listings":watch_list
    })


@login_required
def create(request):
    """Creates a new listing"""
    form = CreateListing()

    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            create = form.save(commit=False)
            create.owner = request.user
            create.save()
            return HttpResponseRedirect(reverse('listing',args=(create.id,)))
        else:
            return render(request, 'auctions/create.html', {"form":form, "message":"Invalid input"})
    # GET
    else:
        return render(request, 'auctions/create.html', {"form":form})


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
