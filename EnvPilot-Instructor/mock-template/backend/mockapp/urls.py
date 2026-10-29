from django.urls import path
from . import views
urlpatterns = [
    path('health/', views.health),
    path('api/login/', views.login),
    path('api/memos/', views.memos),
    path('api/memos/<int:pk>/', views.memo_detail),
    path('api/memos/<int:pk>/archive/', views.archive),
]
