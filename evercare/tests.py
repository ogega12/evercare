from unittest.mock import patch

from django.test import SimpleTestCase

from garage.forms import BookingForm
from garage.views import HomeView


class MissingDatabaseTableFallbackTests(SimpleTestCase):
    @patch('garage.views.connection.introspection.table_names', return_value=[])
    def test_home_view_handles_missing_database_tables(self, _mock_table_names):
        context = HomeView().get_context_data()

        self.assertEqual(list(context['services']), [])
        self.assertEqual(list(context['featured_services']), [])
        self.assertEqual(list(context['promotions']), [])
        self.assertEqual(list(context['gallery_images']), [])
        self.assertEqual(list(context['testimonials']), [])

    @patch('garage.forms.connection.introspection.table_names', return_value=[])
    def test_booking_form_uses_empty_service_queryset_when_table_is_missing(self, _mock_table_names):
        form = BookingForm()

        self.assertEqual(list(form.fields['service'].queryset), [])
