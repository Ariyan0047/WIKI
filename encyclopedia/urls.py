from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:entry>/edit", views.editEntry, name="editEntry"),
    path("randomEntry", views.randomEntry, name="randomEntry"),
    path("searchEntry", views.searchEntry, name="searchEntry")
]
