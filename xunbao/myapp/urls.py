from django.conf.urls import url
from . import views

app_name = 'myapp'

urlpatterns = [
    # xunbao/
    url(r'^$', views.index, name='index'),

    # xunbao/login/
    url(r'^login/$', views.my_login, name='login'),
]
