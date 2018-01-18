from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Problems, Profile
from .forms import AnswerForm

app_name = 'myapp'


@login_required
def index(request):
    problems = Problems.objects.order_by('mydate')
    myprofile = Profile.objects.get(user=request.user)
    count = myprofile.solved
    total = Problems.objects.all().count
    myproblem = problems[0]
    i = 1
    for problem in problems:
        if i == count:
            myproblem = problem
            break
        i = i + 1
    msg = 'Wishing you good luck!'
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['ans'] == myproblem.ans:
                myprofile.solved = count + 1
                myprofile.timetaken = datetime.now()
                myprofile.save()
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                msg = 'Incorrect answer, please try again!'
    else:
        form = AnswerForm()
    return render(request, 'myapp/index.html', {
        'problems': problems,
        'count': count,
        'form': form,
        'msg': msg,
        'total': total,
    })


def my_login(request):
    return render(request, 'myapp/register.html', {})


@login_required
def leaderboard(request):
    profiles = Profile.objects.all()
    return render(request, 'myapp/leaderboard.html', {
        'profiles': profiles,
    })


def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def developers(request):
    return render(request, 'myapp/developers.html',{})
