from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
@login_required
def index(request):
    fname = "production/index.html"
    return render(
			request,
			fname
		)

from .models import (Production,
					ProductionHour)

class ProductionListView(LoginRequiredMixin,ListView):
	model = Production
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Production.objects.filter(Q(job__name__icontains=query) |
									Q(machine__name__icontains=query) |
									Q(description__icontains=query) ).order_by('-created_date')
		return Production.objects.all()

class ProductionDetailView(LoginRequiredMixin,DetailView):
	model = Production


class ProductionHourDetailView(LoginRequiredMixin,DetailView):
	model = ProductionHour


# class ProductGroupListView(ListView):
# 	model = ProductGroup

# class ProductGroupDetailView(DetailView):
# 	model = ProductGroup