import random, os

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .backends import EmailBackend
from django.contrib.auth.decorators import login_required

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from dotenv import load_dotenv

load_dotenv()

config = PangeaConfig(domain=os.getenv("PANGEA_DOMAIN"))

from pangea_django import (
    PangeaAuthentication,
    PangeaAuthMiddleware,
    generate_state_param,
)


def index(request):
    if request.user.is_authenticated:
        return redirect("/shop")

    return redirect(
        f"https://pdn-wil2uqbniob55rhr4fixmlvbk6uya4sy.login.aws.us.pangea.cloud?state={generate_state_param(request)}&redirect_uri="
    )


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
