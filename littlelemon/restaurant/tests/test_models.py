from django.utils import timezone
from django.test import TestCase
from restaurant.models import MenuItem, Booking


class ModelTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), item.title)

    def test_booking(self):
        now = timezone.now()
        #formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        booking = Booking.objects.create(name="aman", no_of_guests=5, booking_date= now)
        print(booking.booking_date)
        self.assertEqual(str(booking), booking.name)