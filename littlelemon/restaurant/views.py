from django.shortcuts import render
from rest_framework import viewsets, permissions

# Create your views here.
from django.http import HttpResponse

from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]