from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/login/$', views.Login.login, name='login'),
    url(r'^login/signup/$', views.Login.signup, name='signup'),
    url(r'^login/verify/$', views.Login.verify, name='verify'),
    url(r'^login/recover/$', views.Login.recover, name='recover'),

    url(r'^matches/getusers/$', views.Matches.get_users, name='get_users'),
    url(r'^matches/getmatches/$', views.Matches.get_matches, name='get_matches'),
    url(r'^matches/loadprofile/$', views.Matches.load_target_profile, name='load_target_profile'),
    url(r'^matches/decision/$', views.Matches.submit_decision, name='submit_decision'),
]