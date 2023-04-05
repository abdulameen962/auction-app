from django.contrib import admin

from . models import *
# Register your models here.
class  ListingAdmin(admin.ModelAdmin):
    list_display = ("id","itemname","price","descr","date","category","state")

class BidAdmin(admin.ModelAdmin):
    filter_horizontal = ("listing",)
    list_display = ("id","userbid")
    
class CommentAdmin(admin.ModelAdmin):
    filter_horizontal = ("comments",)
    
admin.site.register(User)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Listing,ListingAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Category)
