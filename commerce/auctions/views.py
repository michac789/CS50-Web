from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Categories, Auction, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
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


def createlisting_view(request):
    empty0, empty1, empty2 = False, False, False
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = Categories.objects.get(pk=int(request.POST["category"]))
        image_link = request.POST['image_link']
        if title == "":
            empty0 = True
        if description == "":
            empty1 = True
        try:
            starting_bid = float(starting_bid)
        except ValueError:
            empty2 = True
        else:
            empty2 = False
        created = False
        if empty0 == False and empty1 == False and empty2 == False:
            created = True
            Auction.objects.create(title=title, description=description, starting_bid=starting_bid, owner=request.user, category=category, image_link=image_link)
        return render(request, "auctions/createlisting.html", {
            "categories": Categories.objects.all(),
            "created": created,
            "empty0": empty0,
            "empty1": empty1,
            "empty2": empty2
        })
    else:
        return render(request, "auctions/createlisting.html", {
            "categories": Categories.objects.all(),
            "created": False,
            "empty0": empty0,
            "empty1": empty1,
            "empty2": empty2
        })


def auction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    user = User.objects.get(username=request.user)
    watchlist = False
    if user in auction.watchlist.all():
        watchlist = True
    if request.method == "POST":
        x = request.POST["watchlist"]
        if x[0] == '+':
            auction.watchlist.add(user)
            watchlist = True
        else:
            auction.watchlist.remove(user)
            watchlist = False
        return render(request, "auctions/listingpage.html", {
            "auction": auction,
            "watchlist": watchlist
        })
    else:
        return render(request, "auctions/listingpage.html", {
            "auction": auction,
            "watchlist": watchlist
        })


def display_categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all()
    })
    
    
def view_category(request, category):
    return render(request, "auctions/specific_category.html", {
        
    })


def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        
    })
