from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone

# Create your models here.
from product.models import ProductGroup
class Waste(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	productgroup	= models.ForeignKey(ProductGroup,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'wastes')
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Waste'
		verbose_name_plural = 'Waste (Master Data)'

	def __str__(self):
		return ('%s' % (self.name))


def create_waste_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Waste.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, instance.productgroup)
		return create_waste_slug(instance, new_slug=new_slug)
	return slug

def pre_save_waste_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_waste_slug(instance)

pre_save.connect(pre_save_waste_receiver, sender=Waste)