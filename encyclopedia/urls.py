from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.title, name="title"),
    path("new", views.new, name="new"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]
