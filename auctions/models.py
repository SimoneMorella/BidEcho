from django.contrib.auth.models import AbstractUser
from django.db import models
#creare tutti i modelli che servono

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name='watchlist_items', blank=True)

class Categories(models.Model):
    category = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length = 32)
    url_image = models.URLField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_item")
    current_bid = models.FloatField()
    description = models.TextField(max_length = 300)
    in_watchlist = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username", related_name="owner")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at price {self.current_bid} owner:{self.owner}"
    

class Bidding(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username", related_name="person")
    item_bid = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    offer = models.FloatField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username", related_name="commentator")
    item_to_comment = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comment")
    text = models.TextField(max_length = 400)
    created_at = models.DateTimeField(auto_now_add=True)




    