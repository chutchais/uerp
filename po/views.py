from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from .models import Po
class PoListView(ListView):
	model 		= Po
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Po.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(product__name__icontains=query)|
									Q(product__description__icontains=query)).order_by('-created_date')
		return Po.objects.all()

class PoDetailView(DetailView):
	model = Po

def index(request):
    fname = "po/index.html"
    return render(
			request,
			fname
		)
