from django.shortcuts import render, reverse
from django import forms
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404

# Create your views here.
def index(request):
    # raise Http404("Not found oo")
    return render(request, 'renthouse/index.html', {"active": "house"})




class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)


#### Imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from typing import Union
#### Imports

# Signs in user and redirects them to next_page
def sign_in(request, next_page : Union[str, None]='index'):
    '''
        Signs in a user using either username or email address
    '''
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
            if user:
                if user.check_password(password):
                    
                    login(request, user)

                    # Redirect user to requested page (default=index)
                    return HttpResponseRedirect(reverse(f"renthouse:{next_page}"))
            
            msg = 'Username or Password Incorrect. Please, try again'
            
    return render(request, "auth/signin.html", {"form": form, "next_page": next_page, 'msg': msg})


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=50, min_length=5, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, min_length=5, widget=forms.PasswordInput, label='Retype password')
    
#### Imports
from django.contrib.auth.models import User
from .models import UserProfile
#### Imports

def sign_up(request):
    '''
        Signs up a user with care not to create an account with an existing email address or username.
        Also, creates a user profile for the successfully signed up user.
    '''
    form = SignUpForm()
    
    if request.method == 'POST':    
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["password2"]
            
            
            error = False
            
            # Check if username or email already in use
            name_in_use = User.objects.filter(Q(username = username) | Q(username=email)).first()
            if name_in_use:
                err_msg = f'{username} already in use. Please try another username'
                error = True
            email_in_use = User.objects.filter(Q(email=username) | Q(email=email)).first()
            
            if email_in_use:
                err_msg = f'{email} already in use. Please try another email address'
                error = True
            
            if not error:
                if password != password2:
                    err_msg = 'paswords do not match. Please, try again'
                    return render(request, 'auth/signup.html', {'form': form, 'err_msg': err_msg})
                
                
                new_user = User.objects.create_user(username = username, email=email, password=password)
                new_user_profile = UserProfile(user=new_user)
                
                new_user.save()
                new_user_profile.save()
                
                
                ### May need to add some email validation here later
                
                # Not an error message lol, but for lack of words
                err_msg = 'Your Account has been created successfully'
                return render(request, 'auth/signup.html', {'form': form, 'err_msg': err_msg})
            
            else:
                return render(request, 'auth/signup.html', {'form': form, 'err_msg': err_msg})
            

    return render(request, 'auth/signup.html', {'form': form})

from .models import UploadHouse, State, Region, HouseType

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadHouse
        exclude = ["user", "uploaded", "region"]
        
def upload_house(request):
    
    if request.user.is_authenticated:
        
        form = UploadForm()
        active='upload'
        
        if request.method == 'POST':
            form = UploadForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                print(form.cleaned_data)
                region_id = int(request.POST.get("region"))
                selected_region = Region.objects.get(pk=region_id)
                if selected_region:
                    print(selected_region)
                    new_house = form.save(commit=False)
                    new_house.user = request.user
                    new_house.region = selected_region
                    print(new_house)
                    
                    # What to do if form is valid (submitted succefully).
                    new_house.save()
                    #new_house.save()
                    msg= f"{new_house} added successfully"
                # What to do if no selected region
                else:
                    msg = "It seems you submitted a house without a region"
                    
                return render(request, 'rentHouse/upload_house.html', {"form": form, 'active': active, "msg": msg})
            # What to do if form is invalid
            msg = "Invalid submitted form. Please, fill out the form properly"
            
            return render(request, 'rentHouse/upload_house.html', {"form": form, 'active': active, "msg": msg})
            
        return render(request, 'rentHouse/upload_house.html', {"form": form, 'active': active})
    return HttpResponseRedirect(reverse('renthouse:sign_in', args=['upload_house']))



def state_regions(request):
    id = request.GET.get('id')
    if id.isnumeric():
        id = int(id)
        
        # Convert querySet to list
        regions = Region.objects.filter(state__id = id).all()
        regions = list(regions.values())
    else:
        regions = []
    return JsonResponse({'regions': regions})


def view_uploads(request):
    if request.user.is_active:
        active = "viewuploads"
        
        context = {"active": active}
        return render(request, "rentHouse/view_uploads.html", context)
        
    else:
        return HttpResponseRedirect(reverse("renthouse:sign_in", args=["view_uploads"]))
    

    
    