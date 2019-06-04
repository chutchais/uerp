from django.shortcuts import render
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
from .models import Customer

def index(request):
    fname = "customer/index.html"
    return render(
			request,
			fname
		)

class CustomerListView(ListView):
	model = Customer

class CustomerDetailView(DetailView):
	model = Customer
