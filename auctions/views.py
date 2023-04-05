from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import *
        
# def handler404(request, *args, **argv):
#     response = render(request,'auctions/login.html')
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render(request,'auctions/login.html')
#     response.status_code = 500
#     return response

# def handler403(request, *args, **argv):
#     response = render(request,'auctions/login.html')
#     response.status_code = 403
#     return response

# def handler400(request, *args, **argv):
#     response = render(request,'auctions/login.html')
#     response.status_code = 400
#     return response

def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.filter(state=True),
        "closedlistings" : Listing.objects.filter(state=False),
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
            return HttpResponseRedirect(reverse("auction:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auction:index"))


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
        return HttpResponseRedirect(reverse("auction:index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="auction:login")
def create_view(request):
    if request.method == "POST": 
       title = request.POST["title"]
       description = request.POST["descr"]
       bidPrice = request.POST["bid"]
       image = request.FILES["image"]
       category = request.POST["category"]
       user = request.user
       
       if image is None:
           image = ""
           
       newcategory = Category.objects.get(category=category)
       newsave = Listing(itemname=title,descr=description,price=bidPrice,image=image,category=newcategory,winningbid = 0)
       #attempts to create listing
       try:
           newsave.save()
           newsave.createdlist.add(user)
           
       except IntegrityError:
            return render(request,"auctions/create-listing.html",{
            "message": "Something went wrong,pls check all fields again and retry",
            "categories": Category.objects.all(),
       })
       
       return HttpResponseRedirect(reverse("auction:listing", args=(newsave.id, )))
    
    else:
        return render(request,"auctions/create-listing.html",{
            "categories": Category.objects.all(),
        })
    
def listing(request,list_id):
    #since both registered and unregsitered users can visit this view function,a lot of arguments and rendering had to be made to cover for maxbids,adding new bids etc
    user = request.user
    item = Listing.objects.get(pk=list_id)
    watchlists = []
    creator_user = item.createdlist.all()
    creator = creator_user.first()
    #get watchlists is user is authenticated
    if user.is_authenticated:
        watchlists = user.wishitem.all()
    else:
        watchlists = []
    #for bids
    bidlist = []
    ebids = item.bids.all()
    for i in ebids:
        bids = i.bid
        bidlist.append(bids)
    if request.method == "POST":
        newbid = request.POST["bid"]
        exbid = item.price
        
        if int(newbid) > int(exbid):
            #check whether no bid has been made
            if bidlist == []:
                savebid = Bid(bid=newbid,userbid=user)
                savebid.save()
                savebid.listing.add(item)   
                max_user = savebid.userbid
                return render(request, "auctions/listing.html",{
                    "item" : item,
                    "comments": item.views.all(),
                    "bids": item.bids.all().count(),
                    "message": f"Your bid has been successfully added",  
                    "creator" : creator, 
                    "watchlists" : watchlists,
                    "maxuser" : max_user
                })
            else:
                maxbid = max(bidlist)
                mainbid = item.bids.get(bid=maxbid)
                user_winner = mainbid.userbid
                if int(newbid) > maxbid:
                    savebid = Bid(bid=newbid,userbid=user)
                    savebid.save()
                    savebid.listing.add(item)   
                    return render(request, "auctions/listing.html",{
                        "item" : item,
                        "comments": item.views.all(),
                        "bids": item.bids.all().count(),
                        "message": f"Your bid has been successfully added",  
                        "creator" : creator, 
                        "watchlists" : watchlists,
                        "maxuser" : user_winner,
                    })
                else:
                    return render(request, "auctions/listing.html",{
                        "item" : item,
                        "comments": item.views.all(),
                        "bids": item.bids.all().count(),
                        "message": f"Add new bid because bid is lesser than the highest bid which is ${maxbid}",  
                        "creator" : creator, 
                        "watchlists" : watchlists,
                        "maxuser" : user_winner,
                    })
        else: 
            if bidlist == []:
                return render(request,"auctions/listing.html",{
                "item" : item,
                "comments": item.views.all(),
                "bids": item.bids.all().count(),
                "message": f"Bid is less than existing price which is ${item.price}",  
                "creator" : creator, 
                "watchlists" : watchlists,
                })
            else:
                maxbid = max(bidlist)
                mainbid = item.bids.get(bid=maxbid)
                user_winner = mainbid.userbid
                return render(request,"auctions/listing.html",{
                    "item" : item,
                    "comments": item.views.all(),
                    "bids": item.bids.all().count(),
                    "message": f"Bid is less than existing price which is ${item.price}",  
                    "creator" : creator, 
                    "watchlists" : watchlists,
                    "maxuser" : user_winner,
                
                })
    
    else:
        if bidlist == []:
            return render(request,"auctions/listing.html",{
                "item" : item,
                "comments": item.views.all(),
                "bids": f"{item.bids.all().count()}",
                "creator" : creator,
                "watchlists" : watchlists,
            })
        else:
            maxbid = max(bidlist)
            mainbid = item.bids.get(bid=maxbid)
            user_winner = mainbid.userbid
            return render(request,"auctions/listing.html",{
                "item" : item,
                "comments": item.views.all(),
                "bids": f"{item.bids.all().count()}",
                "creator" : creator,
                "watchlists" : watchlists,
                "maxuser" : user_winner,
            })
    
        
@login_required(login_url="auction:login")
def add_watchlist(request,item_id):
    user = request.user
    item = Listing.objects.get(pk=item_id)
    #extra check if watchlist is present already
    watchlists = user.wishitem.all()
    if item not in watchlists:
        item.wishlist.add(user)
        return HttpResponseRedirect(reverse("auction:listing", args=(item.id,)))
    else:
        return HttpResponseRedirect(reverse("auction:listing", args=(item.id,)))
    
@login_required(login_url="auction:login")
def remove_watchlist(request,item_id):
    user = request.user
    item = user.wishitem.get(pk=item_id)
    watchlists = user.wishitem.all()
    #extra check if wishitem is part of watchlists
    if item in watchlists:
        user.wishitem.remove(item)
        return HttpResponseRedirect(reverse("auction:listing", args=(item.id,)))
    else:
        return HttpResponseRedirect(reverse("auction:listing", args=(item.id,)))
    

@login_required(login_url="auction:login")  
def add_comment(request,item_id):
    item = Listing.objects.get(pk=item_id)
    if request.method == "POST":
       com = request.POST["comment"]
       saver = Comment(comment=com)
       saver.save()
       saver.comments.add(item)
       return HttpResponseRedirect(reverse("auction:listing", args=(item.id, )))
   
   
@login_required(login_url="auction:login")  
def close_listing(request,item_id):
    item = Listing.objects.get(pk=item_id)
    user = request.user
    creator_user = item.createdlist.all()
    creator = creator_user.first()
    bidlist = []
    ebids = item.bids.all()
    for i in ebids:
        bids = i.bid
        bidlist.append(bids)
    #server side validation for close listing 
    if user.id == creator.id and item.state == True:
        if bidlist == []:
            inactive = Listing(pk=item_id,itemname=item.itemname,price=item.price,descr=item.descr,date=item.date,image=item.image,category=item.category,state=False,winningbid = 0)
            inactive.save()
        else:
            maxbid = max(bidlist)
            inactive = Listing(pk=item_id,itemname=item.itemname,price=item.price,descr=item.descr,date=item.date,image=item.image,category=item.category,state=False,winningbid = maxbid)
            inactive.save()
        return HttpResponseRedirect(reverse("auction:listing",args=(item.id,)))
    
    else:
        return HttpResponseRedirect(reverse("auction:listing",args=(item.id,)))


@login_required(login_url="auction:login")
def watchlist_view(request):
    user = request.user
    items = user.wishitem.all()
    return render(request,"auctions/watchlist.html",{
        "items" : items,
    })
    
def categories(request):
    category = Category.objects.all()
    return render(request,"auctions/categories.html",{
        "categories": category
    })
    
def category_view(request, list_id):
    categories = Category.objects.get(pk=list_id)
    items = categories.divisions.filter(state=True)
    return render(request,"auctions/index.html",{
        "categorylistings" : items,
        "category" : categories,
        "listings" : Listing.objects.filter(state=True)
    })
    