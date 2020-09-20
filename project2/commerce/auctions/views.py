from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User
from django import forms

class Listform(forms.Form):
    Cats=[
        ('Fa','Fashion'),
        ('To','Toys'),
        ('El','Electronics'),
        ('Ho','Home'),
        ('Cl','clothes'),
    ]
    title=forms.CharField(max_length=64)
    description=forms.Textarea()
    currentprice=forms.IntegerField()
    photo=forms.ImageField(upload_to='biduploads/%Y/%m/%d/',blank=True)
    category=forms.ChoiceField(choices=Cats)
    #models.CharField(choices=Cats,max_length=64)

def index(request):
    return render(request, "auctions/index.html")

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

#@login_required(login_url='login')
@login_required
def listing(request):
    return render(request,"auctions/listing.html",{
        "Lform":Listform()
    })