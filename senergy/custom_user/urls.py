from django.urls import path
from custom_user import views
from rest_framework.authtoken import views as drf_views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('register/', views.register, name='register'),
    path('token/auth/', obtain_jwt_token),
    path('token/refresh/', refresh_jwt_token),
    path('', views.ProfileAPIView.as_view(), name='')
]