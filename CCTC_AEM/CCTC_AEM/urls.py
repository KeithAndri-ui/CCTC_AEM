from django.contrib import admin
from django.urls import path, include
from events import views as event_views  # import your get_started view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Default homepage → get started
    path('', event_views.get_started, name='get_started'),

    # Auth routes (login, signup, logout)
    path('login/', event_views.login_view, name='login'),
    path('signup/', event_views.signup_view, name='signup'),
    path('logout/', event_views.logout_view, name='logout'),

    # Events management
    path('events/', include('events.urls')),  # this points to your events app
]
