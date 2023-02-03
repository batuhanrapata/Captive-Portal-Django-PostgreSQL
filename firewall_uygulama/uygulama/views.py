from django.shortcuts import render
from django.http import request
from django.shortcuts import render, redirect
from .models import User
from .sms_api import *
from .kps_api import *


def login_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        tc_no = request.POST['tc_no']
        birth_date = request.POST['birth_date']
        tel_no = request.POST['tel_no']
        email = request.POST['email']
        confirmation = kps(name, surname, tc_no, birth_date)
        data = User(name=name, surname=surname, tc_no=tc_no, birth_date=birth_date, tel_no=tel_no,
                    confirmation=confirmation, email=email)
        data.save()
        if confirmation:
            verification = send_verification(email)
            return redirect(request, 'templates/sms.html', verification=verification)
        else:
            return 'Kimlik Bilgisi Onaylanmadı!'
    return render(request, 'uygulama/login.html')


def sms(request, verification):
    if request.method == 'POST':
        validation_code = request.POST['validation_code']
        email = request.session.get('email')

        if check_verification_token(email, validation_code):
            return render(request, 'uygulama/page.html')
        else:
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')


def page(request):
    return render(request, 'uygulama/page.html')
