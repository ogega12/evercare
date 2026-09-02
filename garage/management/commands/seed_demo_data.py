from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from garage.models import GalleryImage, Promotion, Service, Testimonial


class Command(BaseCommand):
    help = 'Seed the Evercare Garage site with demo content for the public pages.'

    def handle(self, *args, **options):
        service_data = [
            {
                'name': 'General Service',
                'short_description': 'Routine maintenance for engine health, fluids, filtration and vehicle safety.',
                'description': 'Our general service package covers oil and filter changes, fluid top-ups, tire inspection, brake checks, and a full vehicle walkaround to keep your car running smoothly and safely.',
                'price': None,
                'featured': True,
            },
            {
                'name': 'Engine Diagnostics',
                'short_description': 'Advanced fault-finding for warning lights, power loss and performance issues.',
                'description': 'We use modern scan tools to diagnose engine and electrical issues quickly. From sensor faults to ignition and fuel system problems, we identify the cause before recommending repairs.',
                'price': None,
                'featured': True,
            },
            {
                'name': 'Brake Repair',
                'short_description': 'Inspection and repair of pads, discs, calipers and brake fluid health.',
                'description': 'Your braking system is vital for road safety. We inspect the entire setup, replace worn parts, and test the system to ensure reliable stopping power and quiet operation.',
                'price': None,
                'featured': True,
            },
            {
                'name': 'AC and Cooling',
                'short_description': 'Cooling system checks, gas top-up, and cabin air conditioning service.',
                'description': 'Keep your cabin comfortable and prevent overheating with our cooling system inspections, pressure checks, gas refills, and radiator diagnostics.',
                'price': None,
                'featured': True,
            },
            {
                'name': 'Car Wash',
                'short_description': 'Thorough exterior wash and interior clean for a fresh, well-presented vehicle.',
                'description': 'Our car wash service removes road dirt and grime from your vehicle inside and out, leaving it clean, fresh, and ready for the road.',
                'price': None,
                'featured': False,
            },
            {
                'name': 'Paintwork',
                'short_description': "Professional paintwork care to restore your vehicle's finish and appearance.",
                'description': 'We assess and refresh damaged or faded bodywork with careful paint preparation and colour-matched finishing for a clean, consistent result.',
                'price': None,
                'featured': False,
            },
            {
                'name': 'Buffing',
                'short_description': 'Machine buffing to improve gloss and reduce light surface marks.',
                'description': 'Our buffing service revitalises dull paintwork, removes light surface imperfections, and restores a smooth, glossy finish to your vehicle.',
                'price': None,
                'featured': False,
            },
        ]

        created_services = []
        for item in service_data:
            service, created = Service.objects.get_or_create(
                name=item['name'],
                defaults={
                    'short_description': item['short_description'],
                    'description': item['description'],
                    'price': item['price'],
                    'featured': item['featured'],
                },
            )
            created_services.append(service)

        promo_data = [
            {
                'title': 'Summer Maintenance Pack',
                'description': 'Enjoy reduced pricing on general service and rotating tyre inspection for safe summer driving.',
                'discount': 10,
                'price': 5500,
                'start_date': '2026-09-01',
                'end_date': '2026-09-30',
                'active': True,
            },
            {
                'title': 'Brake Safety Check',
                'description': 'Get a full brake inspection and 10% off replacement parts when you book in this month.',
                'discount': 15,
                'price': 9000,
                'start_date': '2026-09-05',
                'end_date': '2026-10-05',
                'active': True,
            },
        ]

        for item in promo_data:
            Promotion.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'discount': item['discount'],
                    'price': item['price'],
                    'start_date': item['start_date'],
                    'end_date': item['end_date'],
                    'active': item['active'],
                },
            )

        static_dir = Path(__file__).resolve().parents[3] / 'static' / 'images'
        gallery_sources = [
            ('workshop-1.jpg', 'Workshop bay'),
            ('hero.jpg', 'Vehicle inspection'),
            ('about-workshop.jpg', 'Service team'),
            ('service-placeholder.jpg', 'Garage detail'),
        ]

        for filename, caption in gallery_sources:
            image_path = static_dir / filename
            if image_path.exists():
                GalleryImage.objects.get_or_create(
                    title=caption,
                    defaults={
                        'caption': caption,
                        'image': SimpleUploadedFile(
                            filename,
                            image_path.read_bytes(),
                            content_type='image/jpeg',
                        ),
                    },
                )

        testimonials = [
            {
                'name': 'Mary Njeri',
                'review': 'Evercare Garage fixed my car promptly and explained everything clearly. The service was honest and surprisingly smooth.',
                'rating': 5,
                'approved': True,
            },
            {
                'name': 'Daniel Kamau',
                'review': 'I brought in my SUV for diagnostics and the team found the issue quickly. Very professional and efficient.',
                'rating': 5,
                'approved': True,
            },
        ]

        for item in testimonials:
            Testimonial.objects.get_or_create(
                name=item['name'],
                defaults={
                    'review': item['review'],
                    'rating': item['rating'],
                    'approved': item['approved'],
                },
            )

        self.stdout.write(self.style.SUCCESS(f'Seeded {Service.objects.count()} services, {Promotion.objects.count()} promotions, {GalleryImage.objects.count()} gallery items, and {Testimonial.objects.count()} testimonials.'))
