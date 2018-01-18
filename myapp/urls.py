from django.conf.urls import url
from . import views

app_name = 'myapp'

urlpatterns = [
    # xunbao/
    url(r'^$', views.index, name='index'),

    # xunbao/login/
    url(r'^login/$', views.my_login, name='login'),

    # xunbao/leaderboard/
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),

    # logout
    url(r'^logout/$', views.my_logout, name='logout'),

    # /xunbao/developers/
    url(r'^developers/$', views.developers, name='developers'),
]
