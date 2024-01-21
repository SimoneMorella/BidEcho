from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListingEntry", views.listingCreation, name="listingCreation"),
    path("items/<int:item_id>/<str:item_title>", views.item, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addToWatchList/<int:item_id>/<str:item_title>", views.add_to_watchlist, name="add_to_watchlist"),
    path("bid/<int:item_id>/<str:item_title>", views.bid_on_item, name="bid_on_item"),
    path("close/<int:item_id>/<str:item_title>", views.close_bid, name="close_bid"),
    path("closeListings", views.close_listing, name="close_listing"),
    path("comment/<int:item_id>/<str:item_title>", views.add_comment, name="add_comment"),
    path("categories", views.show_categories, name="show_categories"),
    path("categories/<int:category_id>", views.show_category_items, name="show_category_items"),

]
