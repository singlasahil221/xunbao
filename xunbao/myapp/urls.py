from django.conf.urls import url
from . import views

app_name = 'myapp'

urlpatterns = [
    # xunbao/home
    url(r'^$', views.index, name='index'),

    # xunbao/register
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
]