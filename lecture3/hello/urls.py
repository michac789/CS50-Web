from django.urls import path

from . import views

urlpatterns = [
    path("", views.index1, name="index"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david"),
    path("<str:name>", views.greet1, name="greet"),
]
