from django.urls import path
from lab import views
from lab.demo import demo_session
urlpatterns = [
    path('health/', views.health),
    path('api/login/', views.login),
    path('api/demo-session/', demo_session),
    path('api/me/', views.me),
    path('api/projects/', views.projects),
    path('api/environments/', views.environments),
    path('api/environments/<int:pk>/', views.environment_detail),
    path('api/environments/<int:pk>/provision/', views.provision),
    path('api/operations/<int:pk>/', views.operation_detail),
    path('api/assistant/', views.assistant),
]
