from django.shortcuts import render
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from .models import Po
class PoListView(ListView):
	model = Po

class PoDetailView(DetailView):
	model = Po

def index(request):
    fname = "po/index.html"
    return render(
			request,
			fname
		)
