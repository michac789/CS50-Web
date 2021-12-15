from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=32)

class Bid(models.Model):
    bidder = models.CharField(max_length=64)
    price = models.IntegerField(max_length=32)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)

class Comment(models.Model):
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=256)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
