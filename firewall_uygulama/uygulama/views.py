from django.shortcuts import render
from django.http import request
from django.shortcuts import render, redirect
from .models import User, Sms, Log
from .sms_api import *
from .kps_api import *
import subprocess
import http.server
from http.server import HTTPServer
import socket

PORT = 9090  # the port in which the captive portal web server listens
IFACE = "wlan2"  # the interface that captive portal protects
IP_ADDRESS = "172.16.0.1"  # the ip address of the captive portal (it can be the IP of IFACE)


def login_page(request):  # login sayfası (kps doğrulaması)
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        tc_no = request.POST['tc_no']
        birth_date = request.POST['birth_date']
        tel_no = request.POST['tel_no']
        email = request.POST['email']
        confirmation = kps(name, surname, tc_no, birth_date)  # KPS API doğrulaması
        data = User(name=name, surname=surname, tc_no=tc_no, birth_date=birth_date, tel_no=tel_no,
                    confirmation=confirmation, email=email)  # veritabanına kaydet
        data.save()  # veritabanına kaydet
        if confirmation:  # KPS API doğrulaması başarılı
            send_verification(email)  # SMS API mesaj gönder
            return redirect(request, 'templates/sms.html')  # sms sayfasına yönlendir
        else:
            return 'Hatalı Giriş'  # KPS API doğrulaması başarısız
    return render(request, 'uygulama/login.html')


def sms(request):  # sms doğrulama sayfası (sms doğrulaması)
    if request.method == 'POST':
        validation_code = request.POST['validation_code']  # sms doğrulama kodu
        email = request.session.get('email')

        if check_verification_token(email, validation_code):  # SMS API doğrulama
            ipaddress = get_ip()  # ip adresi
            give_permission(ipaddress)  # internet varsa session oluştur
            return redirect(request, 'templates/page.html')
        else:  # doğrulama başarısız
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')


def main_page(request):  # main sayfa (internet varsa)
    return render(request, 'uygulama/page.html')


def give_permission(
        ipadress):  # internet varsa session oluştur ve iptables ayarları yap (internet yoksa iptables iptal edilir)
    # remote_IP = http.server.BaseHTTPRequestHandler.client_address[0]  # remote ip adresi

    remote_IP = ipadress
    # ip adresi bulmak için
    subprocess.call(
        ["iptables", "-t", "nat", "-I", "PREROUTING", "1", "-s", remote_IP, "-j",
         "ACCEPT"])  # iptables ayarları internete erişim için
    subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j", "ACCEPT"])
    ping = os.system("ping -c 1 " + "google.com")
    subprocess.call(["ping", "-c", "1", "google.com"])  # internet var mı kontrolü
    if ping == 0:
        return True  # internet var
    else:
        captive_portal_logout()
        return False  # internet yok


# captive portal logout code
def logout(
        ipadress):  # logout olunca iptables iptal edilir ve login sayfasına yönlendirilir (logout sayfası
    # oluşturulmadı)
    remote_IP = http.server.BaseHTTPRequestHandler.client_address[0]  # remote ip adresi
    subprocess.call(
        ["iptables", "-t", "nat", "-D", "PREROUTING", "-s", remote_IP, "-j", "ACCEPT"])  # iptables iptal edilir
    subprocess.call(["iptables", "-D", "FORWARD", "-s", remote_IP, "-j", "ACCEPT"])
    return redirect(request, 'templates/login.html')


def firewall_logs():  # iptables logları alınır
    iptable_logs = subprocess.call(["iptables", "-L", "-n", "-v", "-x", "-t", "nat"])  # iptables logları
    data = Log(logs=iptable_logs)  # veritabanına kaydet
    data.save()


def captive_portal_start():  # iptables ayarları yapılır ve captive portal başlatılır dockerfile ile yapılabilir
    subprocess.call4(
        ["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])  # dns portu
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
    subprocess.call(
        ["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j",
         "ACCEPT"])  # captive portal portu
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-j", "DROP"])  # diğer tüm paketler iptal edilir
    httpd = HTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler)  # captive portal başlatılır
    subprocess.call(
        ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
         "--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları yapılır

    subprocess.call(
        ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
         "--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları yapılır
    try:  # captive portal başlatılır
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def captive_portal_logout():  # iptables ayarları iptal edilir ve captive portal kapatılır
    subprocess.call(
        ["iptables", "-t", "nat", "-D", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
         "--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları iptal edilir
    subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])
    subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
    subprocess.call(
        ["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j",
         "ACCEPT"])
    subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-j", "DROP"])


# onun ip adresine izin verildi mi(whitelist),//çalışmıyor deneme amaçlı
def check_ip(ipadress):  # remote ip adresi kontrol edilir ve izin verilmişse True döndürülür
    remote_IP = http.server.BaseHTTPRequestHandler.client_address[0]  # remote ip adresi
    if remote_IP in ipadress:
        return True
    else:
        return False


def get_ip():  # ip adresi alınır
    hostname = socket.gethostname()  # hostname
    IPAddr = socket.gethostbyname(hostname)  # ip adresi
    return IPAddr
