from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import UserCreateForm,CoustomLoginForm
from django.views.generic import CreateView,CreateView,DetailView,UpdateView
from . import forms
from django.contrib.auth.views import LoginView



class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "accounts/signup.html"


class CoustomLoginView(LoginView):
    authentication_form = CoustomLoginForm







    



