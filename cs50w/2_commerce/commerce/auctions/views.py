from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

from django import forms
from django.db import connection

class newListing(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'style': 'width: 300px;', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'style':'width: 900px;','class': 'form-control'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Category (e.g. weapon, furniture, medical)', 'style':'width: 900px;','class': 'form-control'}))
    starting_bid = forms.IntegerField()
    image_url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Image URL', 'style': 'width: 300px;', 'class': 'form-control'}))

class newComment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add your thoughts...', 'style':'width: 900px;','class': 'form-control'}))

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        form = newListing(request.POST)
        if form.is_valid():
            item = form.cleaned_data["title"]
            details = form.cleaned_data["description"]
            price = form.cleaned_data["starting_bid"]
            url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            Listing.objects.create(title=item,
                                    description=details,
                                    category=category, 
                                    starting_bid=price,
                                    current_price=price,
                                    image_url=url,
                                    user = request.user
            )
        else:
            return render(request,"auctions/create.html", {
                "form":form
            })
    return render(request, "auctions/create.html", {
        "form":newListing()
    })

def addcomment(request, listing_id):
    post = Comment.objects.filter(listing=listing_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        form = newComment(request.POST)
        if form.is_valid():
            user = request.user
            comment=form.cleaned_data["comment"]
            listing=Listing.objects.get(pk=listing_id)
            Comment.objects.create(
                user=user,
                comment=comment,
                listing=listing
            )
            return render(request, "auctions/listing.html", {
                "listing":listing,
                "comments":post,
                "form":newComment()
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing":listing,
                "comments":post,
                "form":newComment()
            })
        

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    post = Comment.objects.filter(listing=listing_id)
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "comments":post,
        "form":newComment()
    })

def category(request):
    categories = Listing.objects.values('category').distinct()
    return render(request,"auctions/categories.html", {
        "categories":categories
    })

def viewcategory(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html",{
        "listings": listings
    })

def watchlist(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    watcher = request.user

    try:
        user_watchlist = Watchlist.objects.get(user=watcher)
    except:
        user_watchlist = Watchlist.objects.create(user=watcher)

    if request.method == "POST":
        if request.POST.getlist("checkbox") == ["True"]:
            user_watchlist.listing.add(item)
        else:
            user_watchlist.listing.remove(item)

    listings = user_watchlist.listing.all()
    return render(request, "auctions/index.html",{
        "listings": listings
    })


def viewWatchlist(request):
    watcher = request.user
    try:
        user_watchlist = Watchlist.objects.get(user=request.user)
        listings = user_watchlist.listing.all()
    except:
        listings = []
    return render(request, "auctions/index.html",{
        "listings": listings
    })
     
def bid(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    bidder = request.user
    listing = Listing.objects.get(pk=listing_id)
    bid = request.POST.get("bid")
    if request.method == "POST":
        if float(bid) > listing.current_price:
            Bid.objects.create(user=bidder,listing=listing,bid=bid)
            setattr(listing,'current_price',bid)
            listing.save(update_fields=["current_price"])
            return render(request, "auctions/listing.html", {
                "listing": listing
            })
        else:
            return HttpResponse("Your bid was too low")
