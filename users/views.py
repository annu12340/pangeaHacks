import random, os

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from .backends import EmailBackend
from django.contrib.auth.decorators import  login_required

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from dotenv import load_dotenv
load_dotenv()

config = PangeaConfig(domain=os.getenv("PANGEA_DOMAIN"))  

from pangea_django import PangeaAuthentication,PangeaAuthMiddleware, generate_state_param

def index(request):
    if request.user.is_authenticated:
        return redirect("/shop")

    return redirect(f"https://pdn-wil2uqbniob55rhr4fixmlvbk6uya4sy.login.aws.us.pangea.cloud?state={generate_state_param(request)}&redirect_uri=")


def post_login(request):
    user = PangeaAuthentication().authenticate(request=request)
    if user:
        print(3)
        return redirect("/shop")
    print(4)
    return redirect("/")

@login_required(login_url="/")
def logout(request):
    user = PangeaAuthentication().logout(request)
    return redirect("/")

@login_required(login_url="/")
def home(request):
    context = {}
    context["user"] = request.user
    return render(request, "home.html", context)



# def signUp(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:
#         # redirect(f"https://pdn-wil2uqbniob55rhr4fixmlvbk6uya4sy.login.aws.us.pangea.cloud?state={generate_state_param(request)}")
#         # PangeaAuthentication().authenticate(request=request)

#         if request.method == 'POST':
#             username = request.POST.get('username')
#             password1 = request.POST.get('password')
#             password2 = request.POST.get('confirm_password')
#             email = request.POST.get('email')
#             usernameIsUnique = not (User.objects.filter(username=username).exists())
#             emailIsUnique = not (User.objects.filter(email=email).exists())
#             if password1 == password2 and usernameIsUnique and emailIsUnique:
#                 User.objects.create_user(username= username, email=email, password=password1).save()
#                 return redirect('login')
#     context = {}
#     return render(request,'signup.html',context)

# def login(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = EmailBackend().authenticate(request=request,username = username,password = password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect('index')
#     context = {}
#     return render(request, 'login.html', context)

# def logout(request):
    # auth_logout(request)
    # PangeaAuthentication().logout(request)
    return redirect('index')