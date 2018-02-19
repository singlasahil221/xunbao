from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Problems, Profile
from .forms import AnswerForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from .serializers import UserSerializer,LeaderboardSerializers,ProblemsSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.utils.six import BytesIO
import json
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


def leaderboard(request):
    profiles = Profile.objects.all()
    return render(request, 'myapp/leaderboard.html', {
        'profiles': profiles,
    })


def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


def developers(request):
    return render(request, 'myapp/developers.html', {})



@csrf_exempt
def User_list(request):
    if request.method == 'POST':
        prob = json.loads(request.body)
        for user in prob:
            if(user['skey'] != 'abbv'):
                strin = {'response':"0"}
                return JsonResponse(strin,safe=False)
            user = user['email']
            uid , created = User.objects.get_or_create(username=user)
            myprofile = Profile.objects.get(user=uid)
            counter =myprofile.solved
            total = Problems.objects.all().count()
            if total < counter:
                strin = {'response':"you win"}
                return JsonResponse(strin,safe=False)
            print(total,counter)
            Problem = Problems.objects.filter(pk=counter)
            serializer = ProblemsSerializer(Problem, many=True)
            return JsonResponse(serializer.data, safe=False)



@csrf_exempt
def lead_api(request):
    if(request.method == 'GET'):
        users = Profile.objects.all()
        serializer = LeaderboardSerializers(users,many = True)
        return JsonResponse(serializer.data,safe=False)
    else:
        pass


@csrf_exempt
def checkans(request):
    if request.method == 'POST':
        user = json.loads(request.body)
        ans = user['ans']
        if(user['skey'] != 'abbv'):
            strin = {'response':"0"}
            return JsonResponse(strin,safe=False)
        user = user['email']
        problems = Problems.objects.order_by('mydate')
        user = User.objects.get(username=user)           
        myprofile = Profile.objects.get(user=user)
        count = myprofile.solved
        total = Problems.objects.all().count()
        if total < counter:
                strin = {'response':"you win"}
                return JsonResponse(strin,safe=False)
        myproblem = problems[0]
        i = 1
        for problem in problems:
            if i == count:
                myproblem = problem
                break
                i = i + 1
        if ans == myproblem.ans:
            myprofile.solved = count + 1
            myprofile.timetaken = datetime.now()
            myprofile.save()
            strin = {'response':"1"}
            return JsonResponse(strin,safe=False)
        else:      
            strin = {'response':"0"}
            return JsonResponse(strin,safe=False)
    return JsonResponse(user.errors, status=400)



