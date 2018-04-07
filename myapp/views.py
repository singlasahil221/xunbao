from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import Problems, Profile, logs
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
from social_django.models import UserSocialAuth

app_name = 'myapp'


@login_required
def index(request):
    user = request.user
    if not(request.user.is_superuser)and not(user.username.isnumeric()):
        user.username = user.social_auth.get(provider='facebook').uid
        user.save()
    problems = Problems.objects.order_by('mydate')
    myprofile = Profile.objects.get(user=user)
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
            log = logs.objects.create(answer = form.cleaned_data['ans'].lower(),user = request.user)
            log.save()
            if form.cleaned_data['ans'].lower() == myproblem.ans.lower():
                log.status = True
                log.save()
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
            if(user['skey'] != 'sexokashish'):
                strin = [{'response':"0"},]
                return JsonResponse(strin,safe=False)
            fname = user['fname']
            lname = user['lname']
            uid = user['fid']
            user , created = User.objects.get_or_create(username = uid,first_name=fname,last_name=lname)
            myprofile, created = Profile.objects.get_or_create(user=user)
            counter = myprofile.solved
            total = Problems.objects.all().count()
            if total < counter:
                strin = [{'response':"you win"},]
                return JsonResponse(strin,safe=False)
            Problem = Problems.objects.filter(pk=counter)
            serializer = ProblemsSerializer(Problem, many=True)
            return JsonResponse(serializer.data, safe=False)



@csrf_exempt
def lead_api(request):
    if(request.method == 'GET'):
        users = Profile.objects.all().exclude(user__is_superuser = True)
        serializer = LeaderboardSerializers(users,many = True)
        return JsonResponse(serializer.data,safe=False)
    else:
        pass


@csrf_exempt
def checkans(request):
    if request.method == 'POST':
        user = json.loads(request.body)
        ans = user['ans'].lower()
        if(user['skey'] != 'sexokashish'):
            strin = {'response':"0"}
            return JsonResponse(strin,safe=False)
        user = user['email']
        print(ans)
        user = User.objects.get(username = user)
        log = logs.objects.create(answer = ans,user = user)
        log.save()
        problems = Problems.objects.order_by('mydate')          
        myprofile = Profile.objects.get(user=user)
        count = myprofile.solved
        total = Problems.objects.all().count()
        if total < count:
                strin = {'response':"you win"}
                return JsonResponse(strin,safe=False)
        myproblem = problems[0]
        i = 1
        for problem in problems:
            if i == count:
                myproblem = problem
                break
                i = i + 1
        if ans == myproblem.ans.lower():
            log.status = True
            log.save()
            myprofile.solved = count + 1
            myprofile.timetaken = datetime.now()
            myprofile.save()
            strin = {'response':"1"}
            return JsonResponse(strin,safe=False)
        else:      
            strin = {'response':"0"}
            return JsonResponse(strin,safe=False)
    return JsonResponse(user.errors, status=400)

@login_required
def logs_data(request):
    log = logs.objects.all()
    if request.user.is_superuser:
        return render(request,'myapp/logs_data.html',{'logs':log})
    else:
        return HttpResponse('You are not authenticated.')



def status(request):
    if request.method == "GET":
        #return JsonResponse(1,safe = False) #coming soon
        return JsonResponse(2,safe = False) #started
        return JsonResponse(3,safe = False) #end

