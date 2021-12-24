from typing import ItemsView
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
            Auction.objects.create(title=title, description=description, starting_bid=starting_bid, owner=request.user, category=category, image_link=image_link, winner="")
    else:
        created = False
    return render(request, "auctions/createlisting.html", {
        "categories": Categories.objects.all(),
        "created": created,
        "empty0": empty0,
        "empty1": empty1,
        "empty2": empty2
    })


def auction(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(item=auction)
    comments = Comment.objects.filter(item=auction)
    highest_bid = auction.starting_bid
    highest_bidder = None
    total_bids = 0
    for bid in bids:
        total_bids += 1
        if bid.price > highest_bid:
            highest_bid = bid.price
            highest_bidder = bid.bidder.username
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_bids = Bid.objects.filter(bidder=user, item=auction)
        your_latest_bid = 0
        for bid in user_bids:
            if bid.price > your_latest_bid:
                your_latest_bid = bid.price
        watchlist, error, added = False, False, False
        if user in auction.watchlist.all():
            watchlist = True
        if request.method == "POST":
            # Handles add/remove from watchlist
            if request.POST.get('watchlist', False):
                x = request.POST["watchlist"]
                if x[0] == '+':
                    auction.watchlist.add(user)
                    watchlist = True
                else:
                    auction.watchlist.remove(user)
                    watchlist = False
            # Handles bidding process
            elif request.POST.get('bid', False):
                bidding = request.POST["bid"]
                try:
                    bidding = float(bidding)
                except ValueError:
                    error = True
                if not error:
                    if float(bidding) <= auction.starting_bid:
                        error = True
                    for bid in bids:
                        if float(bidding) <= bid.price:
                            error = True
                    if error == False:
                        Bid.objects.create(price=bidding, item=auction, bidder=request.user)
                        added = True
                        bids = Bid.objects.filter(item=auction)
                        highest_bid = auction.starting_bid
                        for bid in bids:
                            if bid.price > highest_bid:
                                highest_bid = bid.price
                                your_latest_bid = bid.price
            # Handles closing bid
            elif request.POST.get('close_bid', False):
                auction.closed = True
                auction.save(update_fields=['closed'])
                auction.winner = highest_bidder
                auction.save(update_fields=['winner'])
            # Handles comments
            elif request.POST.get('comment', False):
                text = request.POST["comment"]
                Comment.objects.create(comment = text, name=request.user, item=auction)
        return render(request, "auctions/listingpage.html", {
            "added": added,
            "error": error,
            "auction": auction,
            "watchlist": watchlist,
            "bids": bids,
            "highest_bid": highest_bid,
            "your_latest_bid": your_latest_bid,
            "total_bids": total_bids,
            "comments": comments
        })
    else:
        return render(request, "auctions/listingpage.html", {
            "auction": auction,
            "comments": comments,
            "highest_bid": highest_bid,
            "total_bids": total_bids
        })


def display_categories(request):
    if request.method == "POST":
        input_category = request.POST["chosen_category"]
        chosen_category = Categories.objects.get(name = input_category)
        relevant_auctions = Auction.objects.filter(category = chosen_category)
        result = 0
        for auction in relevant_auctions:
            result += 1
    else:
        relevant_auctions = None
        result = -1
        chosen_category = ""
    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all(),
        "relevant_auctions": relevant_auctions,
        "result": result,
        "chosen_category": chosen_category
    })


def watchlist(request):
    user = User.objects.get(username=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist_auctions": Auction.objects.filter(watchlist=user)
    })
