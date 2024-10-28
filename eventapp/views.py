from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login as auth_login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import UserProfile, Event, Booking, CustomUser  # Use CustomUser here
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def events(request):
    return render(request, 'events.html')

def booking(request):
    success = False
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        location = request.POST.get('location')
        description = request.POST.get('description')

        Booking.objects.create(
            user=request.user,
            event_name=event_name,
            event_date=event_date,
            location=location,
            description=description
        )
        
        success = True
        messages.success(request, 'Your booking was successful!')

    return render(request, 'booking.html', {'success': success})

def contact(request):
    return render(request, 'contact.html')
@staff_member_required
def admin_dashboard(request):
    bookings = Booking.objects.all()  # Fetch all bookings for admin view
    return render(request, 'admin_dashboard.html', {'bookings': bookings})


def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin')  # Checkbox for admin login

        user = None
        try:
            user = CustomUser.objects.get(username=username_or_email)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=username_or_email)
            except CustomUser.DoesNotExist:
                user = None

        # Authenticate user
        if user is not None and user.check_password(password):
            if is_admin:  # Admin checkbox selected
                if user.is_superuser:

                    auth_login(request, user)
                    messages.success(request, 'Admin login successful!')
                    return (admin_dashboard(request))  # Redirect to admin dashboard
                else:
                    messages.error(request, "Superuser privileges required for admin login.")
            else:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('index')  # Redirect to homepage for regular users
        else:
            messages.error(request, 'Username, email, or password is incorrect.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone_number')  # Ensure you're using the correct field name
            UserProfile.objects.update_or_create(user=user, defaults={'phone_number': phone})
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    return render(request, 'eventapp/event.html', {'events': events})

def book_event(request, event_id):
    if request.user.is_authenticated:
        event = get_object_or_404(Event, id=event_id)
        Booking.objects.create(user=request.user, event=event)
        messages.success(request, f"You have successfully booked {event.title}!")
        return redirect('event_list')
    else:
        messages.warning(request, "You must be logged in to book this event.")
        return redirect('event_list')



@staff_member_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.event_name = request.POST.get('event_name')
        booking.event_date = request.POST.get('event_date')
        booking.location = request.POST.get('location')
        booking.description = request.POST.get('description')
        booking.save()
        messages.success(request, 'Booking updated successfully!')
        return (admin_dashboard(request))  # Redirect to the dashboard after saving
    return render(request, 'edit_booking.html', {'booking': booking})

@staff_member_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully!')
    return (admin_dashboard(request))
