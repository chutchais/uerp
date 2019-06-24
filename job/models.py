from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Sum

# Create your models here.
from product.models 	import Product
from po.models 			import Po
from order.models 		import Order
from recipe.models 		import Recipe 
from machine.models 	import Machine

class Job(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	product			= models.ForeignKey(Product,
							on_delete=models.CASCADE,
							related_name = 'jobs')
	order			= models.ForeignKey(Order,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'jobs')
	qty				= models.IntegerField(default=0)
	recipe			= models.ForeignKey(Recipe,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'jobs')
	# machine			= models.ForeignKey(Machine,
	# 						blank=True,null=True,
	# 						on_delete=models.SET_NULL,
	# 						related_name = 'jobs')

	start_date		= models.DateTimeField(blank=True, null=True)
	stop_date		= models.DateTimeField(blank=True, null=True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)
	# Build Finished Status
	finished		= models.BooleanField(default=False)
	finished_date	= models.DateTimeField(blank=True, null=True)
	# QC checking result
	qc_checked		= models.BooleanField(default=False)
	qc_date			= models.DateTimeField(blank=True, null=True)
	passed			= models.IntegerField(default=0)
	


	def __str__(self):
		return ('%s' % self.name)

	def completed(self):
		# print(self.completes.aggregate(Sum('qty')))
		if self.completes.count()>0 :
			return self.completes.aggregate(Sum('qty'))['qty__sum']
		return 0

	def balance(self):
		# return '%s' % (self.qty - self.completed())
		return self.qty - self.completed()

	def weight(self):
		return self.qty*(self.product.weight+self.product.weight_runner)

	def get_absolute_url(self):
		# return 'test'
		return reverse('job:detail', kwargs={'slug': self.slug})

def pre_save_job_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_job_receiver, sender=Job)


# Means completed from production (Not QA yet)
class Complete(models.Model):
	job 			= models.ForeignKey(Job,
							on_delete=models.CASCADE,
							related_name = 'completes')
	stamp_date		= models.DateTimeField(auto_now_add=True)
	qty				= models.IntegerField(default=0)
	description 	= models.TextField(null = True,blank = True)

	def __str__(self):
		return ('%s-%s' % (self.job,self.qty))



# To collect RAW mat of Job.
# from recipe.models import RecipeItem
# class RawMaterialUsage(models.Model):
# 	job				= models.ForeignKey(Job,
# 							on_delete=models.CASCADE,
# 							related_name = 'rawusages')
# 	recipeitem		= models.ForeignKey(RecipeItem,
# 							null = True,blank = True,
# 							on_delete=models.SET_NULL,
# 							related_name = 'rawusages')
# 	planed			= models.DecimalField(default=0,max_digits=8, decimal_places=3)
# 	actual			= models.DecimalField(default=0,max_digits=8, decimal_places=3)
# 	lot 			= models.CharField(max_length=50,null = True,blank = True)
# 	created_date	= models.DateTimeField(auto_now_add=True)
# 	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
# 	active			= models.BooleanField(default=True)

# 	def __str__(self):
# 		return ('%s-%s' % (self.job,self.recipeitem))





