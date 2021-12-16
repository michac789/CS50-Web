from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    categories = (
        ('FA', 'Fashion'),
        ('TO', 'Toys'),
        ('EL', 'Electronics'),
        ('HO', 'Home'),
        ('AR', 'Arts'),
        ('SU', 'Supplies'),
        ('ED', 'Education'),
        ('MI', 'Miscellaneous')
    )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=32, choices=categories)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_bid = models.IntegerField(max_length=32)
    
    def __str__(self):
        return f"({self.id}). {self.title} ({self.category}): {self.description}"

class Bid(models.Model):
    price = models.IntegerField(max_length=32)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.bidder}: {self.item}, {self.price}"

class Comment(models.Model):
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=256)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
