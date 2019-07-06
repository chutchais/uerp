from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import Customer

@login_required
def index(request):
    fname = "customer/index.html"
    return render(
			request,
			fname
		)

class CustomerListView(LoginRequiredMixin,ListView):
	model = Customer
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Customer.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(address__icontains=query) |
									Q(delivery_address__icontains=query) |
									Q(tax__icontains=query)).order_by('-created_date')
		return Customer.objects.all()

class CustomerDetailView(LoginRequiredMixin,DetailView):
	model = Customer
