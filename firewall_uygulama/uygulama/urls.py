from django.urls import path

from . import views
from .views import login_page

app_name = 'uygulama'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('sms/', views.sms, name='sms'),
    path('page/', views.main_page, name='page'),
    path('mail/', views.mail, name='mail'),
    path('singed_out/', views.SingedOutView.as_view(), name='singed_out'),
]
