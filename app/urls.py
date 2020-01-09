from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index),
    # path('slack/oauth/', views.slack_oauth),
    path('events/', views.Events.as_view()),
]