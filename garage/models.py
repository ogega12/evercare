from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('garage:service_detail', args=[self.slug])

    @property
    def default_image(self):
        image_keywords = (
            (('brake',), 'images/brakes.jpg'),
            (('diagnostic',), 'images/engine diagnosis.jpg'),
            (('engine repair',), 'images/engine repairr.jpg'),
            (('transmission', 'gearbox'), 'images/transmission.jpg'),
            (('suspension', 'shock', 'steering'), 'images/suspension.jpg'),
            (('ac', 'air conditioning', 'cooling'), 'images/car AC.jpg'),
            (('electrical', 'battery'), 'images/elecricals.jpg'),
            (('wash', 'detailing'), 'images/carwash.jpg'),
            (('buff', 'polish'), 'images/buffing.jpg'),
            (('paint', 'bodywork'), 'images/paintwork.jpg'),
            (('general', 'service', 'maintenance'), 'images/car service.jpg'),
        )
        service_name = self.name.casefold()
        for keywords, image_path in image_keywords:
            if any(keyword in service_name for keyword in keywords):
                return image_path
        return 'images/service-placeholder.jpg'


class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title or f'Image {self.pk}'


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} ({self.rating})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    vehicle_registration = models.CharField(max_length=50, blank=True)
    vehicle_make = models.CharField(max_length=100, blank=True)
    vehicle_model = models.CharField(max_length=100, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    custom_service = models.CharField(max_length=200, blank=True)
    preferred_date = models.DateField(blank=True, null=True)
    preferred_time = models.TimeField(blank=True, null=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        service_name = self.service.name if self.service else self.custom_service or 'No service'
        return f"{self.full_name} - {service_name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject or 'Contact'}"
