from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("category", views.category,name="category"),
    path("category/<str:category>", views.viewcategory,name="viewcategory"),
    path("listings/<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("mywatchlist", views.viewWatchlist,name="mywatchlist"),
    path("listings/<int:listing_id>/bid", views.bid,name="bid"),
    path("listings/<int:listing_id>/addcomment",views.addcomment,name="addcomment")
]
