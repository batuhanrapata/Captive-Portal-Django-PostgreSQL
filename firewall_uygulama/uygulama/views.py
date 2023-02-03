from django.shortcuts import render
from django.http import request
from django.shortcuts import render, redirect
from .models import User, Sms
from .sms_api import *
from .kps_api import *
import subprocess
import requests
import time


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


def sms(request):
    if request.method == 'POST':
        validation_code = request.POST['validation_code']
        email = request.session.get('email')
        name = request.session.get('name')
        confirmation = check_verification_token(email, validation_code)
        data = Sms(sms_code=validation_code, confirmation=confirmation)
        data.save()
        if confirmation:
            remote_ip = "clienti ip"  # user ip
            subprocess.call(["iptables", "-t", "nat", "-I", "PREROUTING", "1", "-s", remote_ip, "-j", "ACCEPT"])
            subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_ip, "-j", "ACCEPT"])
            return redirect(request, 'uygulama/page.html', name=name)
        else:
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')


def page(request):
    keep_alive()
    return render(request, 'uygulama/page.html')


def keep_alive():
    while True:
        try:
            # Keep alive request
            response = requests.get("http://www.example.com")
            if response.status_code == 200:
                print("Keep alive successful")
            else:
                print("Keep alive failed")
        except:
            print("Keep alive failed")
        # Wait for next keep alive attempt
        time.sleep(30)
