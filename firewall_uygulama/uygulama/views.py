from django.http import request
from django.shortcuts import render, redirect
from .models import User, Sms, Log
from .sms_api import *
from .kps_api import *
import subprocess
import http.server
from http.server import HTTPServer
import socket
import time

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
            give_permission(ipaddress)  # internet varsa session oluştur //oluşturulmadı sadece iptables ayarları var
            return redirect(request, 'templates/page.html')
        else:  # doğrulama başarısız
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')


# 5dk da bir session süresi uzatılır kontrol edilir loglar veritabanına kaydedilir // deneme amaçlı mantık değişebilir
def sleep_5_min(request):
    timeout_session(request)
    firewall_logs()  # firewall loglarını veritabanına kaydet
    time.sleep(300)
    return


def main_page(request):  # main sayfa (tüm verification başarılı olursa yönlendirilecek sayfa)
    return render(request, 'uygulama/page.html')


def give_permission(ipadress):  # internet varsa session oluştur ve iptables ayarları yap
    # remote_IP = http.server.BaseHTTPRequestHandler.client_address[0]  # remote ip adresi //bu kod iptal edildi

    remote_IP = ipadress
    subprocess.call(
        ["iptables", "-t", "nat", "-I", "PREROUTING", "1", "-s", remote_IP, "-j",
         "ACCEPT"])  # iptables ayarları internete erişim için
    subprocess.call(["iptables", "-I", "FORWARD", "-s", remote_IP, "-j", "ACCEPT"])
    ping = os.system("ping -c 1 " + "google.com")
    subprocess.call(["ping", "-c", "1", "google.com"])  # internet var mı kontrolü
    if ping == 0:
        return True  # internet var
    else:
        return False  # internet yok


# captive portal logout code
def logout(
        ipadress):  # logout olunca iptables iptal edilir ve login sayfasına yönlendirilir (logout sayfası
    # oluşturulmadı)
    remote_IP = ipadress
    # remote_IP = http.server.BaseHTTPRequestHandler.client_address[0]  # remote ip adresi //bu kod satırı iptal edildi
    subprocess.call(
        ["iptables", "-t", "nat", "-D", "PREROUTING", "-s", remote_IP, "-j", "ACCEPT"])  # iptables iptal edilir
    subprocess.call(["iptables", "-D", "FORWARD", "-s", remote_IP, "-j", "ACCEPT"])
    return redirect(request, 'templates/login.html')


def firewall_logs():  # iptables logları alınır
    iptable_logs = subprocess.call(["iptables", "-L", "-n", "-v", "-x", "-t", "nat"])  # iptables logları
    data = Log(logs=iptable_logs)  # veritabanına kaydet
    data.save()


def get_ip():  # ip adresi alınır permission verilmesi için!
    hostname = socket.gethostname()  # hostname
    IPAddr = socket.gethostbyname(hostname)  # ip adresi
    return IPAddr


def captive_portal_start():  # iptables ayarları yapılır ve captive portal başlatılır dockerfile ile yapılabilir
    subprocess.call(
        ["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])  # dns portu
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
    subprocess.call(
        ["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j",
         "ACCEPT"])  # captive portal portu
    subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-j", "DROP"])  # diğer tüm paketler iptal edilir
    httpd = HTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler)  # captive portal başlatılır
    subprocess.call(
        ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
         "--to-destination", IP_ADDRESS + ":" + str(PORT)])
    subprocess.call(
        ["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
         "--to-destination", IP_ADDRESS + ":" + str(PORT)])
    try:  # captive portal başlatılır
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def captive_portal_stop():  # iptables ayarları iptal edilir ve captive portal kapatılır
    subprocess.call(
        ["iptables", "-t", "nat", "-D", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
         "--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları iptal edilir
    subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])
    subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
    subprocess.call(
        ["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j",
         "ACCEPT"])
    subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-j", "DROP"])


def is_logged_in(request):  # oturum açıp açmadığını kontrol eder
    if 'name' in request.session:
        return True
    else:
        return False


# timeout session
def timeout_session(request):
    if is_logged_in(request):
        request.session.set_expiry(360)  # 360 saniye sonra oturum sonlanır
    else:
        pass  # session timeout
