from django.urls import path
from . import views



urlpatterns = [
    path('', views.homepage, name='home'),
    path('log-in/', views.log_in, name='log_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('submit_signin', views.submit_signin, name='submit_signin'),
    path('submit_signup', views.submit_signup, name='submit_signup'),
    path('allowed', views.allowed, name='allowed'),
    path('protected', views.protected, name='protected'),
    path('logout/', views.logout_view, name='logout'),
]