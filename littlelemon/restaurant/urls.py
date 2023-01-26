from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'booking', views.BookingViewSet)

app_name = 'restaurant'

urlpatterns = [
    path('menu-items/', views.MenuItemListCreateView.as_view(), name="menu"),
    path('menu-items/<int:pk>', views.MenuItemRetrieveUpdateDestroyView.as_view(), name="menu-item"),
    path('booking/', include(router.urls)),
]