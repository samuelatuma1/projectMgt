from django.shortcuts import render, reverse
from django import forms
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
# Create your views here.
def index(request):
    # raise Http404("Not found oo")
    return render(request, 'renthouse/index.html', {"active": "house"})

def upload_house(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('renthouse:sign_in', args=['upload_house']))
    return HttpResponse("Upload House")


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from typing import Union

# Signs in user and redirects them to next_page
def sign_in(request, next_page : Union[str, None]='index'):
    form = SignInForm()
    msg = None
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            formdata : dict = form.cleaned_data
            username : str= formdata.get("username")
            password : str = formdata.get("password")
            next_page : str = request.POST.get("next")
            
            user = User.objects.filter(Q(username=username) | Q(email=username)).first()
            
            if user.check_password(password):
                
                login(request, user)

                # Redirect user to requested page (default=index)
                return HttpResponseRedirect(reverse(f"renthouse:{next_page}"))
            
            msg = 'Username or Password Incorrect. Please, try again'
            
    return render(request, "auth/signin.html", {"form": form, "next_page": next_page, 'msg': msg})