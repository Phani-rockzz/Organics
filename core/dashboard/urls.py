from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [

    path('staff/home/', views.home, name='home'),
    path('staff/orders/', views.orders, name='orders'),

]