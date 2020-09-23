from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,listing,bids
from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.db.models import Avg, Max, Min, Sum

class Listform(ModelForm):
    class Meta:
        model = listing
        exclude=['user']

class Bidform(ModelForm):
    class Meta:
        model = bids
        fields=['bid']

def index(request):
    if request.method=="POST":
        #item=listing(user=request.user)# way2
        #Lform=Listform(request.POST,request.FILES,instance=item)# way2
        Lform=Listform(request.POST,request.FILES)# way1
        if Lform.is_valid():
            item=Lform.save(commit=False)# way1
            item.user = request.user# way1
            item.save()
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

def itempage(request,id):
    if request.method == "POST":
        if request.POST["action"]=="Place Bid":
            Bform=Bidform(request.POST)
            if Bform.is_valid():
                bid=Bform.save(commit=False)
                bid.user = request.user
                bid.product=listing.objects.get(id=id)
                bid.save()
                return HttpResponseRedirect(reverse('itempage',args=(id,)))
        elif request.POST["action"]=="Close Auction":
            pass
    else:
        item=listing.objects.get(id=id)
        bidlist=bids.objects.filter(product=id)
        if bidlist:
            aux=bids.objects.all().aggregate(Max('bid'))['bid__max']
            maxbid=bids.objects.get(bid=aux)
        else:
            maxbid=None
        user=request.user
        return render(request,"auctions/item.html",{
            "item":item,
            "Bform":Bidform(),
            "bids":bidlist,
            "maxbid":maxbid,
            "user":user,
        })
