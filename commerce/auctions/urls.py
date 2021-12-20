from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting_view, name="createlisting"),
    path("<int:auction_id>", views.auction, name="auction"),
    path("categories", views.display_categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist")
]
