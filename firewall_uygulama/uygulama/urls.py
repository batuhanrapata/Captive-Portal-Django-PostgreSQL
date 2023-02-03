from django.urls import path

from . import views

app_name = 'uygulama'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('sms/', views.sms, name='sms'),
    path('page/', views.page, name='page')
]
