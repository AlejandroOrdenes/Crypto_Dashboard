
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home' ),
    path('logIn/', views.logIn, name='logIn'),
    path('signIn/', views.signIn, name='signIn'),
    path('signout/', views.signout, name='signout'),
    path('dashboard/', views.dashboardCrypto, name='dashboard'),
    path('portfolio/', views.portfolio, name='portfolio'),
]