from django.urls import path
from sleep import views

urlpatterns = [
    path('', views.sleep_record, name='SleepRecord'),
]
