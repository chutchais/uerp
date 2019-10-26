from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
import datetime

# Create your views here.
@login_required
@permission_required('production.view_production')
def index(request):
    fname = "production/index.html"
    #     # modified_date__gt= datetime.datetime.today()-datetime.timedelta(days=30)
    production_list 	= Production.objects.select_related('job__product__group').filter(
    						active= True ,finished = False,
    						modified_date__gt= datetime.datetime.today()-datetime.timedelta(days=7)
    					).order_by('job__product__group','created_date')
    return render(
			request,
			fname,
			{
				'object_list' : production_list
			}
		)

from .models import (Production,
					ProductionHour)

class ProductionListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	# model = Production
	queryset = Production.objects.select_related()
	paginate_by = 100
	permission_required = ('production.view_production')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Production.objects.filter(Q(job__name__icontains=query) |
									Q(machine__name__icontains=query) |
									Q(description__icontains=query) ).order_by('-created_date')
		return Production.objects.select_related()

class ProductionDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	# model = Production
	queryset = Production.objects.select_related()
	permission_required = ('production.view_production')


class ProductionHourDetailView(LoginRequiredMixin,DetailView):
	# model = ProductionHour
	queryset = ProductionHour.objects.select_related()


# class ProductGroupListView(ListView):
# 	model = ProductGroup

# class ProductGroupDetailView(DetailView):
# 	model = ProductGroup