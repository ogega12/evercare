# Generated data migration to backfill missing Service slugs

from django.db import migrations
from django.utils.text import slugify


def backfill_slugs(apps, schema_editor):
    """Generate slugs for any Service records that don't have one."""
    Service = apps.get_model('garage', 'Service')
    services_without_slug = Service.objects.filter(slug__isnull=True) | Service.objects.filter(slug='')
    
    for service in services_without_slug:
        service.slug = slugify(service.name)
        service.save(update_fields=['slug'])


def reverse_backfill(apps, schema_editor):
    """Reverse migration: clear slugs that were auto-generated."""
    # We don't clear slugs on reverse, as they may have been set manually.
    # This is a one-way data fix.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0003_booking_custom_service'),
    ]

    operations = [
        migrations.RunPython(backfill_slugs, reverse_backfill),
    ]

