from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:topic>", views.entry, name="entry"),
    path("results/", views.result, name="result")
]
