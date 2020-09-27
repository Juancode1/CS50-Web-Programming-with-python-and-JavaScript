from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,listing,bids,sold,watchlistM
from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.db.models import Avg, Max, Min, Sum
import datetime

class Listform(ModelForm):
    class Meta:
        model = listing
        exclude=['user']
        widgets = {'terminated': forms.HiddenInput()}

class Bidform(ModelForm):
    class Meta:
        model = bids
        fields=['bid']

def index(request):
    if request.user.is_authenticated:
        Wlist=watchlistM.objects.filter(watcher=request.user).all()
    else:
        Wlist=[]
    
    Lsold=sold.objects.all()
    hoy=datetime.datetime.now() 
    Nmessage=None
    for item in Lsold:
        if item.buyer==request.user:
            Nmessage.append(f"You have won the bid on { item.product } with a bid of {item.price}")
        
        #if hoy-item.solddate>datetime.timedelta(days=3): # after 3 days from the sell of the item it will be deleted
            #pr=listing.objects.get(title=item.product)
            #pr.delete()

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
            "items":listing.objects.all(),
            "Nmessage":Nmessage,
            "Wlist":Wlist,
            "Cats":listing.Cats,
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
                "message": "Invalid username and/or password.",
                "Cats":listing.Cats,
            })
    else:
        return render(request, "auctions/login.html",{
            "Cats":listing.Cats,
        })

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
                "message": "Passwords must match.",
                "Cats":listing.Cats,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "Cats":listing.Cats,
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html",{
            "Cats":listing.Cats,
        })

#@login_required(login_url='login')
@login_required
def setitem(request):
    Wlist=watchlistM.objects.filter(watcher=request.user).all()
    return render(request,"auctions/listing.html",{
        "Lform":Listform(),
        "Wlist":Wlist,
        "Cats":listing.Cats,
    })

def itempage(request,id):
    Wlist=watchlistM.objects.filter(watcher=request.user).all() 
    item=listing.objects.get(id=id)
    bidlist=bids.objects.filter(product=id)
    aux=item.currentprice
    if bidlist:
        aux=bids.objects.filter(product=id).aggregate(Max('bid'))['bid__max']
        maxbid=bids.objects.get(product=id,bid=aux)
    else:
        maxbid=None
    user=request.user
    Bform=Bidform()
    Emessage=None
    if Wlist.filter(product=item).count()>0:
        watchFlag=True
    else:
        watchFlag=False
    
    if item.terminated and maxbid==None:
        Amessage=f"The Auction is Officially Closed, No Auction winner. No Bids Placed"
    elif item.terminated and maxbid!=None:
        Amessage=f"The Auction is Officially Closed, the Auction winner is {maxbid.user} with ${maxbid.bid} bid"
    else:
        Amessage=None
      
    if request.method == "POST":
        if request.POST["action"]=="Place Bid":
            Bform=Bidform(request.POST)
            if Bform.is_valid():
                if int(request.POST["bid"])>aux :
                    bid=Bform.save(commit=False)
                    bid.user = request.user
                    bid.product=listing.objects.get(id=id)
                    bid.save()
                    return HttpResponseRedirect(reverse('itempage',args=(id,)))
                else:
                    Emessage="Bid Gotta be Higher than the Current Bid"
        
        elif request.POST["action"]=="Close Auction":
            if maxbid:
                winner=sold(product=item,seller=item.user,buyer=maxbid.user,price=maxbid.bid)
                winner.save()
                item.terminated=True
                item.save() 
                return HttpResponseRedirect(reverse('itempage',args=(id,)))
            else:
                item.terminated=True
                item.save()
                return HttpResponseRedirect(reverse('itempage',args=(id,)))

        elif request.POST["action"]=="Add to Watchlist":
            watch=watchlistM(product=item,watcher=user)
            watch.save()
            return HttpResponseRedirect(reverse('itempage',args=(id,)))
        elif request.POST["action"]=="Remove from Watchlist":
            watch=watchlistM.objects.get(product=item,watcher=user)
            watch.delete()
            return HttpResponseRedirect(reverse('itempage',args=(id,)))
    
    return render(request,"auctions/item.html",{
        "item":item,
        "Bform":Bform,
        "bids":bidlist,
        "maxbid":maxbid,
        "user":user,
        "Emessage":Emessage,
        "Amessage":Amessage,
        "Wlist":Wlist,
        "watchFlag":watchFlag,
        "Cats":listing.Cats,
    })

@login_required
def watchlist(request):
    Wlist=watchlistM.objects.filter(watcher=request.user).all()
    return render(request,'auctions/watchlist.html',{
        "Wlist":Wlist,
        "Cats":listing.Cats,
    })
def category(request,cat):
    if request.user.is_authenticated:
        Wlist=watchlistM.objects.filter(watcher=request.user).all()
    else:
        Wlist=[]
    items=listing.objects.filter(category=cat).all()
    return render(request,'auctions/Category.html',{
         "items":items,
         "category":cat,
         "Cats":listing.Cats,
         "Wlist":Wlist,
     })