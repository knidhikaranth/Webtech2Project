from django import forms
from django.forms import ModelForm
from catalog.models import Movies, Users, Ratings
class RegisterForm(forms.ModelForm):
	class Meta:
		model = Users
		fields = ["username", "email", "password"]