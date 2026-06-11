from django.urls import path

from . import views

app_name = "fora"

urlpatterns = [
    path("book/", views.book_view, name="book"),
    path("book/confirmation/<int:pk>/", views.confirmation_view, name="confirmation"),
]
