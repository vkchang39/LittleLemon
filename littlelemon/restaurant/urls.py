from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.MenuItemListCreateView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemRetrieveUpdateDestroyView.as_view()),
]