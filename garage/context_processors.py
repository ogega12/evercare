from django.conf import settings

def global_settings(request):
    return {
        'WHATSAPP_NUMBER': settings.WHATSAPP_NUMBER,
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
