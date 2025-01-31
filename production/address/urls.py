from django.urls import path
from . import views


urlpatterns = [
    path('address', views.add_address, name='address'),
  
]
