from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('register/', views.register.as_view(), name='register'),
    path('accounts/login/', views.CustomLogin.as_view(), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name="index"),
    path('league/<str:leagueCode>', views.leaguePage, name="leaguePage"),
    path('team/<str:teamID>', views.teamPage, name="teamPage"),
    path('teamsapi/', views.teamsAPI, name="teamsAPI"),
]
