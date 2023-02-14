from django.urls import path

from . import views
from .views import *

app_name = 'uygulama'

urlpatterns = [
    path('login/', login_view.as_view(), name='login'),
    path('sms/', views.sms, name='sms'),
    path('page/', main_page_view.as_view(), name='page'),
    path('mail/', mail_view.as_view(), name='mail'),
    path('singed_out/', views.SingedOutView.as_view(), name='singed_out'),
    path('send_mail', views.send_mail, name='send_mail'),
]
