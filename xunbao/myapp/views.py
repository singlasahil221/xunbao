from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import Problems

app_name = 'myapp'


@login_required
def index(request):
    return render(request, 'myapp/index.html', {})


def my_login(request):
    return render(request, 'myapp/register.html', {})

