from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return f"{self.id}: {self.name}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_bid = models.FloatField(max_length=32)
    image_link = models.CharField(max_length=128, default=None)
    
    def __str__(self):
        return f"{self.id}. {self.owner}: {self.title} ({self.category}), starting bid: {self.starting_bid}"

class Bid(models.Model):
    price = models.FloatField(max_length=32)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="person")
    
    def __str__(self):
        return f"{self.bidder}: {self.item}, {self.price}"

class Comment(models.Model):
    comment = models.CharField(max_length=256)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
