from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from .models import Delivery
class DeliveryListView(ListView):
	model 		= Delivery
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Delivery.objects.filter(Q(invoice__icontains=query) |
									Q(description__icontains=query) |
									Q(po__product__name__icontains=query)).order_by('-created_date')
		return Delivery.objects.all()

class DeliveryDetailView(DetailView):
	model = Delivery

def index(request):
    fname = "delivery/index.html"
    return render(
			request,
			fname
		)