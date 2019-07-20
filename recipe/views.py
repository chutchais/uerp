from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView


from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
from .models import Recipe

@login_required
@permission_required('recipe.can_view')
def index(request):
    fname = "recipe/index.html"
    recipe_list = Recipe.objects.filter(
    					active = True
    					).order_by('prod_group','name')
    return render(
			request,
			fname,
			{
				'object_list' : recipe_list
			}
		)

class RecipeListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	model = Recipe
	paginate_by = 100
	permission_required = ('recipe.can_view','recipe.can_edit','recipe.can_add')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Recipe.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) ).order_by('-created_date')
		return Recipe.objects.all()

class RecipeDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	model = Recipe
	permission_required = ('recipe.can_view','recipe.can_edit','recipe.can_add')