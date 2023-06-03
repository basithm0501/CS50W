from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:topic>", views.entry, name="entry"),
    path("results/", views.result, name="result"),
    path("newpage/", views.newpage, name="newpage"),
    path("edit/<str:topic>", views.edit, name="edit"),
    path("rand/", views.rand, name="rand")
]
