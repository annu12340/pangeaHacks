import random, os

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from .backends import EmailBackend
from django.contrib.auth.decorators import  login_required

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services.authn.authn import AuthN

from dotenv import load_dotenv
load_dotenv()
config = PangeaConfig(domain=os.getenv("PANGEA_DOMAIN"))  


def index(request):
    return render(request,'index.html')


# @login_required(login_url='login')
# def homePage(request):
#     if request.method == 'POST':
#         title = request.POST.get('frontText')
#         content = request.POST.get('backText')
#         subject = request.POST.get('subject')

#         owner = request.user.email
#         FlashCard.objects.create(title=title,content=content,subject=subject,owner=owner)
#         return redirect('homePage')
#     users = FlashCard.objects.filter(owner= request.user.email)
#     subjects = FlashCard.objects.values('subject').distinct()[:5]
#     context = {'users': users,'subjects':subjects}
#     return render(request, 'index.html', context)


def signUp(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    # if request.user.is_authenticated:
    #     return redirect('index')
    # else:

    #     if request.method == 'POST':
    #         username = request.POST.get('username')
    #         password1 = request.POST.get('password')
    #         password2 = request.POST.get('confirm_password')
    #         email = request.POST.get('email')
    #         usernameIsUnique = not (User.objects.filter(username=username).exists())
    #         emailIsUnique = not (User.objects.filter(email=email).exists())
    #         if password1 == password2 and usernameIsUnique and emailIsUnique:
    #             User.objects.create_user(username= username, email=email, password=password1).save()
    #             return redirect('login')

    context = {}
    return render(request,'signup.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = EmailBackend().authenticate(request=request,username = username,password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
    context = {}
    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('index')