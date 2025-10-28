from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('update/<int:pk>/', views.update_event, name='update_event'),
    path('delete/<int:pk>/', views.delete_event, name='delete_event'),
   

]
