from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('reviews/', views.reviews, name='reviews'),
    path('leave-review/', views.leave_review, name='leave_review'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
]
