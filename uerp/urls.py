"""uerp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/',include(('customer.urls','customer'),namespace='customer')),
    path('delivery/',include(('delivery.urls','delivery'),namespace='delivery')),
    path('job/',include(('job.urls','job'),namespace='job')),
    path('order/',include(('order.urls','order'),namespace='order')),
    path('recipe/',include(('recipe.urls','recipe'),namespace='recipe')),
    path('product/',include(('product.urls','product'),namespace='product')),
    path('po/',include(('po.urls','po'),namespace='po')),
]

admin.site.site_header = 'uProduction - ERP system'
admin.site.site_title = "uProduction Admin"
admin.site.index_title = "Welcome to uProduction ERP Portal"