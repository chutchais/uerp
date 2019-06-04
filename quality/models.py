from django.db import models
from django.urls import reverse
from django.db.models import Sum

# Create your models here.
from job.models import Job

class Inspection(models.Model):
	description 	= models.TextField(null = True,blank = True)
	job				= models.OneToOneField(Job,
							on_delete=models.CASCADE,
							related_name = 'inspection')
	passed			= models.IntegerField(default=0)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)
	to_warehouse	= models.BooleanField(default=False)
	to_date			= models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return ('%s' % self.job.name)

	def get_absolute_url(self):
		# return 'test'
		return reverse('job:detail', kwargs={'slug': self.slug})


