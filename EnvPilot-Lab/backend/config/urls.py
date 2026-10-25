from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from lab import views
from lab.demo import DemoSession
urlpatterns = [
    path('health/', views.health),
    path('api/login/', obtain_auth_token),
    path('api/demo-session/', DemoSession.as_view()),
    path('api/me/', views.Me.as_view()),
    path('api/projects/', views.Projects.as_view()),
    path('api/environments/', views.Environments.as_view()),
    path('api/environments/<int:pk>/', views.EnvironmentDetail.as_view()),
    path('api/environments/<int:pk>/provision/', views.Provision.as_view()),
    path('api/operations/<int:pk>/', views.OperationDetail.as_view()),
    path('api/assistant/', views.Assistant.as_view()),
]
