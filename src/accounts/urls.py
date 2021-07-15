from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="profile"),
    path('create-profile/', views.create_profile, name="create-profile"),
    path('update-profile/', views.update_profile, name="update-profile"),


]