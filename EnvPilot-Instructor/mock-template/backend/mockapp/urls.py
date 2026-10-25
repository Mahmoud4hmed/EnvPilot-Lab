from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import health, Memos, MemoDetail, Archive
urlpatterns = [path('health/', health),path('api/login/',obtain_auth_token),path('api/memos/',Memos.as_view()),path('api/memos/<int:pk>/',MemoDetail.as_view()),path('api/memos/<int:pk>/archive/',Archive.as_view())]
