from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm
from datetime import date


# ---------- AUTH VIEWS ----------
def get_started(request):
    # If the user is already logged in, redirect to the dashboard
    if request.user.is_authenticated:
        return redirect('event_list')
    return render(request, 'get_started.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'registration/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('event_list')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- EVENT CRUD VIEWS ----------
@login_required(login_url='login')
def event_list(request):
    query = request.GET.get('q', '')
    date_filter = request.GET.get('date', '')
    sort = request.GET.get('sort', '')

    events = Event.objects.all()

    # Filtering by query
    if query:
        events = events.filter(title__icontains=query) | events.filter(description__icontains=query)

    # Filtering by date
    if date_filter:
        events = events.filter(date=date_filter)

    # Sorting logic
    if sort == 'date_asc':
        events = events.order_by('date')
    elif sort == 'date_desc':
        events = events.order_by('-date')
    elif sort == 'title_asc':
        events = events.order_by('title')
    elif sort == 'title_desc':
        events = events.order_by('-title')
    else:
        events = events.order_by('date')  # default sort

    # --------- Dashboard Analytics ---------
    today = date.today()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()

    context = {
        'events': events,
        'query': query,
        'date_filter': date_filter,
        'sort': sort,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }

    return render(request, 'events/event_list.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

def about_view(request):
    return render(request, 'about.html')
