from django.contrib import admin
from django.urls import path


from .views import CustomerListView,CustomerDetailView

urlpatterns = [
    path('', CustomerListView.as_view(), name='list'),
    path('<slug:slug>', CustomerDetailView.as_view(), name='detail'),
]
