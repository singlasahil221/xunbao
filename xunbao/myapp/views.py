from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views.generic import View

from .forms import UserForm

app_name = 'myapp'


@login_required
def index(request):
    return render(request, 'myapp/index.html', {})


class UserFormView(View):
    form_class = UserForm
    template_name = 'myapp/register.html'

    # displays blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned (normalised) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # return User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('myapp:index'))
        return render(request, self.template_name, {'form': form})
