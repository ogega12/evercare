from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.conf import settings
from .models import Service, Promotion, GalleryImage, Testimonial, Booking, ContactMessage
from .forms import BookingForm, ContactForm

class HomeView(TemplateView):
    template_name = 'garage/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()[:6]
        context['featured_services'] = Service.objects.filter(featured=True)[:4]
        context['promotions'] = Promotion.objects.filter(active=True)
        context['gallery_images'] = GalleryImage.objects.all()[:6]
        context['testimonials'] = Testimonial.objects.filter(approved=True)[:5]
        # Example counters
        context['stats'] = {
            'years': 10,
            'vehicles': 12500,
            'technicians': 12,
            'awards': 4,
        }
        context['whatsapp'] = settings.WHATSAPP_NUMBER
        context['google_maps_key'] = settings.GOOGLE_MAPS_API_KEY
        return context

class AboutView(TemplateView):
    template_name = 'garage/about.html'

class ServiceListView(ListView):
    model = Service
    template_name = 'garage/services.html'
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'garage/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        context['related_services'] = Service.objects.exclude(pk=service.pk)[:3]
        return context

class GalleryView(ListView):
    model = GalleryImage
    template_name = 'garage/gallery.html'
    context_object_name = 'images'

class PromotionsView(ListView):
    model = Promotion
    template_name = 'garage/offers.html'
    context_object_name = 'promotions'

class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = 'garage/booking.html'
    success_url = reverse_lazy('garage:booking')

    def get_initial(self):
        initial = super().get_initial()
        service_id = self.request.GET.get('service')
        if service_id:
            try:
                service = Service.objects.get(pk=service_id)
            except Service.DoesNotExist:
                service = None
            else:
                initial['service'] = service
        return initial

    def form_valid(self, form):
        booking = form.save()
        messages.success(self.request, 'Thank you! Your booking/enquiry has been received. We will contact you soon.')
        return redirect(self.success_url)

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'garage/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us. We will respond shortly.')
            return redirect('garage:contact')
        return render(request, 'garage/contact.html', {'form': form})


class AdminLoginView(View):
    template_name = 'garage/admin_login.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('garage:admin_dashboard')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, 'Welcome back to the admin dashboard.')
                return redirect('garage:admin_dashboard')
            form.add_error(None, 'This login is for staff/admin accounts only.')
        return render(request, self.template_name, {'form': form})


class AdminLogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('garage:admin_login')


class AdminDashboardView(View):
    template_name = 'garage/admin_dashboard.html'

    @method_decorator(staff_member_required(login_url='garage:admin_login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        testimonials = Testimonial.objects.order_by('-date')
        bookings = Booking.objects.select_related('service').order_by('-created_at')[:10]
        contact_messages = ContactMessage.objects.order_by('-created_at')[:10]

        context = {
            'testimonials': testimonials,
            'bookings': bookings,
            'contact_messages': contact_messages,
            'total_testimonials': testimonials.count(),
            'pending_reviews': testimonials.filter(approved=False).count(),
            'open_bookings': Booking.objects.filter(status__in=['pending', 'contacted', 'confirmed', 'in_progress']).count(),
            'pending_interactions': ContactMessage.objects.filter(handled=False).count(),
            'status_choices': Booking.STATUS_CHOICES,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        testimonial_id = request.POST.get('testimonial_id')
        booking_id = request.POST.get('booking_id')
        contact_id = request.POST.get('contact_id')
        review_edit_id = request.POST.get('review_edit_id')
        review_delete_id = request.POST.get('review_delete_id')
        contact_edit_id = request.POST.get('contact_edit_id')
        contact_delete_id = request.POST.get('contact_delete_id')

        if review_delete_id:
            testimonial = get_object_or_404(Testimonial, pk=review_delete_id)
            testimonial_name = testimonial.name
            testimonial.delete()
            messages.success(request, f'Review by {testimonial_name} was deleted.')
            return redirect('garage:admin_dashboard')

        if review_edit_id:
            testimonial = get_object_or_404(Testimonial, pk=review_edit_id)
            name = request.POST.get('review_name', '').strip()
            review_text = request.POST.get('review_text', '').strip()
            rating = request.POST.get('review_rating')

            if name and review_text and rating:
                testimonial.name = name
                testimonial.review = review_text
                testimonial.rating = int(rating)
                testimonial.save(update_fields=['name', 'review', 'rating'])
                messages.success(request, f'Review by {testimonial.name} was updated.')
            else:
                messages.error(request, 'Review name, text and rating are required.')
            return redirect('garage:admin_dashboard')

        if contact_delete_id:
            contact_message = get_object_or_404(ContactMessage, pk=contact_delete_id)
            contact_name = contact_message.name
            contact_message.delete()
            messages.success(request, f'Customer interaction from {contact_name} was deleted.')
            return redirect('garage:admin_dashboard')

        if contact_edit_id:
            contact_message = get_object_or_404(ContactMessage, pk=contact_edit_id)
            name = request.POST.get('contact_name', '').strip()
            email = request.POST.get('contact_email', '').strip()
            subject = request.POST.get('contact_subject', '').strip()
            message = request.POST.get('contact_message', '').strip()

            if name and email and message:
                contact_message.name = name
                contact_message.email = email
                contact_message.subject = subject
                contact_message.message = message
                contact_message.save(update_fields=['name', 'email', 'subject', 'message'])
                messages.success(request, f'Customer interaction from {contact_message.name} was updated.')
            else:
                messages.error(request, 'Customer name, email and message are required.')
            return redirect('garage:admin_dashboard')

        if testimonial_id:
            testimonial = get_object_or_404(Testimonial, pk=testimonial_id)
            testimonial.approved = not testimonial.approved
            testimonial.save(update_fields=['approved'])
            action = 'approved' if testimonial.approved else 'hidden from the public'
            messages.success(request, f'Review by {testimonial.name} was {action}.')

        elif booking_id:
            booking = get_object_or_404(Booking, pk=booking_id)
            selected_status = request.POST.get('status')
            if selected_status in dict(Booking.STATUS_CHOICES):
                booking.status = selected_status
                booking.save(update_fields=['status'])
                messages.success(request, f'Booking for {booking.full_name} updated to {booking.get_status_display()}.')

        elif contact_id:
            contact_message = get_object_or_404(ContactMessage, pk=contact_id)
            contact_message.handled = not contact_message.handled
            contact_message.save(update_fields=['handled'])
            action = 'marked as handled' if contact_message.handled else 'reopened'
            messages.success(request, f'Contact message from {contact_message.name} was {action}.')

        return redirect('garage:admin_dashboard')


# Custom error pages
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)