from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.loadpage, name="loadpage"),
    path("random", views.random, name="random"),
    path("newpage", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("wiki/<str:name>/edit", views.edit, name="edit"),
    path("wiki/<str:name>/confirmedit", views.confirmedit, name="confirmedit")
]
