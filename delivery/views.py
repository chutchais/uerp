from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
from .models import Delivery

@login_required
@permission_required('delivery.view_delivery')
def index(request):
    fname = "delivery/index.html"
    delivery_list 	= Delivery.objects.select_related('po__product__group').filter(
    						active= True
    					).order_by('po__product__group','created_date')
    return render(
			request,
			fname,
			{
				'object_list' : delivery_list
			}
		)

class DeliveryListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	# model 		= Delivery
	queryset = Delivery.objects.select_related()
	paginate_by = 100
	permission_required = ('delivery.view_delivery')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Delivery.objects.select_related('po').filter(Q(invoice__icontains=query) |
									Q(description__icontains=query) |
									Q(po__name__icontains=query) |
									Q(po__product__name__icontains=query)).order_by('-created_date')
		return Delivery.objects.select_related()

class DeliveryDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	# model = Delivery
	queryset = Delivery.objects.select_related()
	permission_required = ('delivery.view_delivery')

