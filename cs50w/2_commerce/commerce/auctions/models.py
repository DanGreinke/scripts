from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    current_price = models.DecimalField(max_digits=9, decimal_places=2)
    image_url = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title} {self.description}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"{self.user} {self.listing}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=14, decimal_places=2)
    def __str__(self):
        return f"{self.user} {self.listing} {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    
    def __str__(self):
        return f"{self.user} {self.listing} {self.comment}"


