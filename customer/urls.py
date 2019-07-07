from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required


from .views import CustomerListView,CustomerDetailView,index

urlpatterns = [
    path('', login_required()(index), name='index'),
    path('list/', login_required()(CustomerListView.as_view()), name='list'),
    path('<slug:slug>', login_required()(CustomerDetailView.as_view()), name='detail'),
]
