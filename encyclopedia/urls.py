from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random")
]
