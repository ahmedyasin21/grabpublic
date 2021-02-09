from django.shortcuts import render
from django.urls import reverse_lazy
# from .models import UserProfile
from .forms import UserCreateForm,CoustomLoginForm
from django.views.generic import CreateView,CreateView,DetailView,UpdateView
from . import forms
from django.contrib.auth.views import LoginView
# from django.contrib.auth.decorators import login_required
# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "accounts/signup.html"


class CoustomLoginView(LoginView):
    authentication_form = CoustomLoginForm


# @login_required
# def userprofile(request):
#     u_form =UserUpdateForm
#     p_form = UserProfileForm()

#     context ={
#         'u_form':u_form,
#         'p_form' :p_form
#     }
#     return render(request,"accounts/userprofile.html")





    



