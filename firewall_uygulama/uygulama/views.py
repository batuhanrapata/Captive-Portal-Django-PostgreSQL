from django.shortcuts import render
from django.http import request
from django.shortcuts import render, redirect
from .models import User
from .sms_api import *
from .kps_api import *
import subprocess


def login_page(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        tc_no = request.POST['tc_no']
        birth_date = request.POST['birth_date']
        tel_no = request.POST['tel_no']
        email = request.POST['email']
        confirmation = kps(name, surname, tc_no, birth_date)  # KPS API
        data = User(name=name, surname=surname, tc_no=tc_no, birth_date=birth_date, tel_no=tel_no,
                    confirmation=confirmation, email=email)
        data.save()  # veritabanına kaydet
        if confirmation:  # KPS API doğrulaması
            verification = send_verification(email)  # SMS API mesaj gönder
            return redirect(request, 'templates/sms.html')  # sms sayfasına yönlendir
        else:
            return 'Kimlik Bilgisi Onaylanmadı!'
    return render(request, 'uygulama/login.html')


def sms(request): # sms doğrulama
    if request.method == 'POST':
        validation_code = request.POST['validation_code'] # sms doğrulama kodu
        email = request.session.get('email')

        if check_verification_token(email, validation_code): # SMS API doğrulama
            keep_alive(request)  # internet varsa session oluştur
            return redirect(request, 'templates/page.html')
        else:  # doğrulama başarısız
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')


def page(request):
    return render(request, 'uygulama/page.html')


def keep_alive(request): # internet varsa session oluştur
    remote_IP = request.META.get('REMOTE_ADDR')  # remote ip adresi
    ping = os.system("ping -c 1 " + "google.com")
    subprocess.call(["ping", "-c", "1", "google.com"])
    subprocess.call(["iptables", "-t", "nat", "-I", "PREROUTING", "1", "-s", remote_IP, "-j", "ACCEPT"])
    subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j", "ACCEPT"])
    if ping == 0:
        return True  # internet var
    else:
        return False  # internet yok
