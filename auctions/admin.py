from django.contrib import admin
from .models import Listing, User, Bidding, Comment, Categories

# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bidding)
admin.site.register(Comment)
admin.site.register(Categories)