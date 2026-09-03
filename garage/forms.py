from django import forms
from django.db import connection, ProgrammingError, OperationalError
from .models import Booking, ContactMessage, Service


def _service_queryset():
    try:
        if Service._meta.db_table not in connection.introspection.table_names():
            return Service.objects.none()
    except (ProgrammingError, OperationalError):
        return Service.objects.none()
    return Service.objects.order_by('name')


class BookingForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=_service_queryset(),
        empty_label='Select a service',
        required=False,
        label='Choose a service'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = _service_queryset()

    custom_service = forms.CharField(
        max_length=200,
        required=False,
        label='Or type the service you need'
    )
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Preferred date'
    )
    preferred_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True,
        label='Preferred time'
    )

    class Meta:
        model = Booking
        fields = ['full_name', 'phone', 'email', 'vehicle_registration', 'vehicle_make', 'vehicle_model', 'service', 'custom_service', 'preferred_date', 'preferred_time', 'message']
        labels = {
            'full_name': 'Full name',
            'phone': 'Phone number',
            'email': 'Email address',
            'vehicle_registration': 'Vehicle registration',
            'vehicle_make': 'Vehicle make',
            'vehicle_model': 'Vehicle model',
            'message': 'Additional notes',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        custom_service = cleaned_data.get('custom_service', '').strip()

        if not service and not custom_service:
            raise forms.ValidationError('Please choose a service or type the service you need.')

        return cleaned_data

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
