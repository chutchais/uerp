from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import Delivery

@login_required
def index(request):
    fname = "delivery/index.html"
    delivery_list 	= Delivery.objects.filter(
    						active= True
    					).order_by('po__product__group','created_date')
    return render(
			request,
			fname,
			{
				'object_list' : delivery_list
			}
		)

class DeliveryListView(LoginRequiredMixin,ListView):
	model 		= Delivery
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Delivery.objects.filter(Q(invoice__icontains=query) |
									Q(description__icontains=query) |
									Q(po__product__name__icontains=query)).order_by('-created_date')
		return Delivery.objects.all()

class DeliveryDetailView(LoginRequiredMixin,DetailView):
	model = Delivery

