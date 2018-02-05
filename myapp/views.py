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
def User_list(request,pk):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        uid = User.objects.filter(email=pk)
        snippets = Profile.objects.filter(user=uid)
        Problem = Problems.objects.filter(pk=1)
        #count = int(snippets)
        serializer = UserSerializer(Problem, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def lead_api(request):
    if(request.method == 'GET'):
        users = Profile.objects.all()
        serializer = LeaderboardSerializers(users,many = True)
        return JsonResponse(serializer.data,safe=False)
    else:
        pass


@csrf_exempt
def checkans(request,user,pk):
    if request.method == "GET":
        problems = Problems.objects.order_by('mydate')
        user = User.objects.filter(email=user)
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
        if pk == myproblem.ans:
            myprofile.solved = count + 1
            myprofile.timetaken = datetime.now()
            myprofile.save()
            return JsonResponse(1,safe=False)
        else:            
            return JsonResponse(0,safe=False)
