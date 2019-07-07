from django.shortcuts import render
from django import forms

from django.contrib.auth.decorators import login_required

# @login_required
def index(request):
	return render(request, 'index.html')


# If you don't do this you cannot use Bootstrap CSS
from django.contrib.auth.forms import AuthenticationForm 
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))