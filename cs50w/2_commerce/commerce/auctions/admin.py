from django.contrib import admin
from .models import Bid, Comment, User, Listing, Watchlist

class BidAdmin(admin.ModelAdmin):
    list_display = ("user","listing","bid")

class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "starting_bid",
        "current_price",
        "image_url",
        "user"
        )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user","listing","comment")

# Register your models here.
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist)