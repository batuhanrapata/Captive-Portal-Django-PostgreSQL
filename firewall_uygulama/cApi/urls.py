
from django.urls import path

from . import views
from .views import *

app_name = 'cApi'

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('log/', LogView.as_view(), name='log'),
    path('email/', EmailView.as_view(), name='email'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('django_user/', djangoUserView.as_view(), name='django_user'),
]
