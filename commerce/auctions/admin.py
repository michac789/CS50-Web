from django.contrib import admin
from django.contrib.admin.filters import ListFilter
from .models import Auction, Bid, Comment

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    pass #to add (?)
    
class BidAdmin(admin.ModelAdmin):
    pass

admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
