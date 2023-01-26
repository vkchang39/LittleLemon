from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import MenuItem, Booking
from restaurant.serializers import MenuItemSerializer, BookingSerializer


MENU_URL = reverse('restaurant:menu')
BOOKING_URL = reverse('restaurant:booking-list')

def menu_detail_url(menu_id):
    return reverse('restaurant:menu-item', args=[menu_id])

def booking_detail_url(booking_id):
    return reverse('restaurant:booking-detail', args=[booking_id])

def create_menuItem(**params):
    defaults = {
        'title': 'Sample title',
        'price': Decimal('5.25'),
        'inventory': 5,
    }
    defaults.update(params)

    menuItem = MenuItem.objects.create(**defaults)
    return menuItem

def create_booking(**params):
    now = timezone.now()
    #formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    defaults = {
        'name': 'sample name',
        'no_of_guests': 5,
        'booking_date': now
    }
    defaults.update(params)

    booking = Booking.objects.create(**defaults)
    return booking


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicMenuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(MENU_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required(self):
        res = self.client.get(BOOKING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMenuAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', username='aman', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrive_menu(self):
        create_menuItem()
        create_menuItem()

        res = self.client.get(MENU_URL)

        menuItem = MenuItem.objects.all().order_by('id')
        serializer = MenuItemSerializer(menuItem, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrive_booking(self):
        create_booking()
        create_booking()

        res = self.client.get(BOOKING_URL)

        booking = Booking.objects.all().order_by('id')
        serializer = BookingSerializer(booking, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_menu_detail(self):
        menuItem = create_menuItem()

        url = menu_detail_url(menuItem.id)
        res = self.client.get(url)

        serializer = MenuItemSerializer(menuItem)
        self.assertEqual(res.data, serializer.data)

    def test_get_booking_detail(self):
        booking = create_booking()

        url = booking_detail_url(booking.id)
        res = self.client.get(url)
        #body = res.data
        #booking_date = body['booking_date']
        #body['booking_date']= f'{ booking_date : %Y-%m-%d %H:%M:%S}'

        serializer = BookingSerializer(booking)
        self.assertEqual(res.data, serializer.data)

    def test_create_menu(self):
        payload = {
            'title': 'Sample recipe',
            'inventory': 30,
            'price': Decimal('5.99'),
        }
        res = self.client.post(MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        menuItem = MenuItem.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(menuItem, k), v)

    def test_create_booking(self):
        now = timezone.now()
        #formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        payload = {
            'name': 'Sample name',
            'no_of_guests': 5,
            'booking_date': now
        }
        res = self.client.post(BOOKING_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(id=res.data['id'])
        for k, v in payload.items():
            #print(v)
            self.assertEqual(getattr(booking, k), v)

    def test_partial_update(self):
        menuItem = create_menuItem()

        payload = {'title': 'New recipe title'}
        url = menu_detail_url(menuItem.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        menuItem.refresh_from_db()
        self.assertEqual(menuItem.title, payload['title'])

    def test_full_update(self):
        menuItem = create_menuItem()

        payload = {
            'title': 'Sample recipe title',
            'inventory': 20,
            'price': Decimal('2.50')
            }
        url = menu_detail_url(menuItem.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        menuItem.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(menuItem, k), v)

    def test_delete_recipe(self):
        menuItem = create_menuItem()

        url = menu_detail_url(menuItem.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MenuItem.objects.filter(id=menuItem.id).exists())

    def test_delete_booking(self):
        booking = create_booking()

        url = booking_detail_url(booking.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MenuItem.objects.filter(id=booking.id).exists())