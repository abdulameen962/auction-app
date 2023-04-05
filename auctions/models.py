from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.category}"
    
    
class Listing(models.Model):
    itemname = models.CharField(max_length=64)
    price = models.IntegerField()
    descr = models.CharField(max_length=500, default=None)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/items", default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="divisions", default=None)
    wishlist = models.ManyToManyField(User,blank=True, related_name="wishitem")
    createdlist = models.ManyToManyField(User,blank=True, related_name="createditem")
    state = models.BooleanField(default=True)
    winningbid = models.IntegerField(default=None)
    
    def __str__(self):
        return f"{self.itemname} has the price of {self.price} on {self.date} whose description is {self.descr} and looks like {self.image} which is under {self.category} and it is {self.state}"
    
class Bid(models.Model):
    bid = models.IntegerField()
    userbid = models.ForeignKey(User,on_delete=models.CASCADE,default=None,related_name="wagers")
    listing = models.ManyToManyField(Listing, blank=True, related_name="bids")  
    
    def __str__(self):
        return f"{self.bid} made by {self.userbid}"
    
class Comment(models.Model):
    comment = models.CharField(max_length=500)
    comments = models.ManyToManyField(Listing, blank=True,related_name="views")
    
    def __str__(self):
        return f"{self.comment}"
    
    