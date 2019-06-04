from django.contrib import admin
from django.urls import path


from .views import index,PoListView,PoDetailView

urlpatterns = [
    path('', index, name='index'),
    path('list/', PoListView.as_view(), name='list'),
    path('<slug:slug>', PoDetailView.as_view(), name='detail'),
]
