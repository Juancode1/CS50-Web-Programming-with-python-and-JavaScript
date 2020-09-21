from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,listing
from django import forms
from django.forms import ModelForm
from django.conf import settings

"""
class Listform(forms.Form):
    Cats=[
        ('Fa','Fashion'),
        ('To','Toys'),
        ('El','Electronics'),
        ('Ho','Home'),
        ('Cl','clothes'),
    ]
    title=forms.CharField(max_length=64,label="Item Name")
    description=forms.Textarea()
    currentprice=forms.IntegerField(label="Price" )
    photo=forms.ImageField(required=True,label="Picture")
    category=forms.ChoiceField(choices=Cats,label="Category")"""

class Listform(ModelForm):
    class Meta:
        model = listing
        fields = ['user','title', 'description','currentprice','photo','category']

def index(request):
    if request.method=="POST":
        Lform=Listform(request.POST,request.FILES)
        if Lform.is_valid():
            user=settings.AUTH_USER_MODEL
            Lform.save()
            #item=listing(user=user)
            #item.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/index.html",{
            "items":listing.objects.all()
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

#@login_required(login_url='login')
@login_required
def setitem(request):
    return render(request,"auctions/listing.html",{
        "Lform":Listform()
    })