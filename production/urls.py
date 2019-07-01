from django.contrib import admin
from django.urls import path


from .views import (ProductionListView,
					ProductionDetailView,
					ProductionHourDetailView,
					index)

urlpatterns = [
    path('', index, name='list'),
    path('list/', ProductionListView.as_view(), name='list'),
    path('<int:pk>', ProductionDetailView.as_view(), name='detail'),
    path('hour/<int:pk>', ProductionHourDetailView.as_view(), name='hour'),
]
