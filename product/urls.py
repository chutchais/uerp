from django.contrib import admin
from django.urls import path


from .views import (ProductListView,
					ProductDetailView,
					ProductGroupListView,
					ProductGroupDetailView,
					index)

urlpatterns = [
    path('', index, name='index'),
    path('list/', ProductListView.as_view(), name='list'),
    path('group', ProductGroupListView.as_view(), name='group-list'),
    path('<slug:slug>', ProductDetailView.as_view(), name='detail'),
]
