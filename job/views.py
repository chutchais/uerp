from django.shortcuts import render
from django.db.models import Q,F
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.utils import timezone
# Create your views here.
from .models import Job,Complete
from recipe.models import Recipe
from quality.models import Inspection

def index(request):
    fname = "job/index.html"
    return render(
			request,
			fname
		)

class JobListView(ListView):
	model = Job
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Job.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(product__name__icontains=query)|
									Q(product__description__icontains=query) |
									Q(order__name__icontains=query)).order_by('-created_date')
		return Job.objects.all()

class JobDetailView(DetailView):
	model = Job
	def get_context_data(self, **kwargs):
		context     			= super().get_context_data(**kwargs)
		job 					= self.get_object()
		context['recipe_list'] 	= Recipe.objects.filter(prod_group=job.product.group)
		# print(context['recipe_list'])
		return context

class JobDeleteView(DeleteView):
	model = Job
	# success_url = reverse_lazy('job:list')
	def get_success_url(self):
		redirect = self.request.GET.get('next')
		# print (redirect)
		return redirect

def update_job_finished(requets,slug):
	job 		= Job.objects.get(slug=slug)
	redirect	= requets.GET.get('next')
	status		= requets.GET.get('status')
	job.finished = True if status =='true' else False
	job.finished_date = timezone.now() if status =='true' else None
	job.save()
	return HttpResponseRedirect(redirect)




def update_recipe(requets,slug):
	job 		= Job.objects.get(slug=slug)
	recipe 		= Recipe.objects.get(slug=requets.POST.get('recipe'))
	redirect	= requets.GET.get('next')
	job.recipe  = recipe
	job.save()
	return HttpResponseRedirect(redirect)

def reset_recipe(requets,slug):
	redirect	= requets.GET.get('next')
	job 		= Job.objects.get(slug=slug)
	job.recipe  = None
	job.save()
	print(redirect)
	return HttpResponseRedirect(redirect)


def add_job_complete(requets,slug):
	job 		= Job.objects.get(slug=slug)
	redirect	= requets.GET.get('next')
	qty			= requets.POST.get('qty')
	description = requets.POST.get('description')
	# print(qty,description)
	Complete.objects.create(job=job,qty=qty,description=description,stamp_date=timezone.now())
	return HttpResponseRedirect(redirect)

def delete_job_complete(requets,slug,pk):
	redirect	= requets.GET.get('next')
	c=Complete.objects.get(pk=pk)
	c.delete()
	return HttpResponseRedirect(redirect)


def add_job_inspection(requets,slug):
	job 		= Job.objects.get(slug=slug)
	redirect	= requets.GET.get('next')
	qty			= requets.POST.get('qty')
	description = requets.POST.get('description')
	# print(qty,description)
	Inspection.objects.create(job=job,passed=qty,description=description,
			to_warehouse=True,to_date=timezone.now())
	# Increase Qty in Warehouse
	product = job.product
	product.increase_qty(int(qty))
	# product.save()
	return HttpResponseRedirect(redirect)

def delete_job_inspection(requets,slug):
	redirect	= requets.GET.get('next')
	job 		= Job.objects.get(slug=slug)
	i=Inspection.objects.get(job = job)
	qty = i.passed
	i.delete()
	# Decrease Qty in warehouse
	product = job.product
	product.decrease_qty(int(qty))

	return HttpResponseRedirect(redirect)