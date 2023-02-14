from django.http import request
from django.shortcuts import render, redirect
from .models import User, Sms, Log, email_verification
from .sms_api import *
from .kps_api import *
import subprocess
import socket
from .mailgun_api import send_simple_message
from django.views import generic
from .login_form import LoginForm
from .email_form import MailForm
from django.http import HttpResponse

PORT = 9090  # the port in which the captive portal web server listens
IFACE = "wlan2"  # the interface that captive portal protects
IP_ADDRESS = "172.16.0.1"  # the ip address of the captive portal (it can be the IP of IFACE)


def login_page(request):  # login sayfası (kps doğrulaması)
    form = LoginForm()
    form = {'form': form}
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            global name, email, data
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            tc_no = form.cleaned_data['tc_no']
            birth_date = form.cleaned_data['birth_date']
            tel_no = form.cleaned_data['tel_no']
            email = form.cleaned_data['email']
            confirmation = kps(name, surname, tc_no, birth_date)  # KPS API doğrulaması
            data = User(name=name, surname=surname, tc_no=tc_no, birth_date=birth_date, tel_no=tel_no,
                        confirmation=confirmation, email=email)
            data.save()
            if confirmation:  # KPS API doğrulaması başarılı
                global otp
                otp = send_simple_message(email)  # Mail API mesaj gönder

                return redirect('uygulama:mail')  # mail sayfasına yönlendir
            else:
                return HttpResponse('<b> Hatalı Kimlik Bilgisi Girişi </b>')  # KPS API doğrulaması başarısız

    return render(request, 'uygulama/login.html', form)


def mail(request):
    form = MailForm()
    form = {'form': form}
    if request.method == 'POST':
        otp_verification = request.POST['otp']
        if otp == otp_verification:  # SMS API doğrulama
            global verification_data
            verification_data = email_verification(user=data, email_code=otp, confirmation=True)
            verification_data.save()  # email doğrulama kodu doğruysa veritabanına kaydet
            global ipaddress
            ipaddress = get_ip()
            give_permission(ipaddress)  # internet varsa session oluştur //oluşturulmadı sadece iptables ayarları var
            return redirect('uygulama:page')
        else:
            return HttpResponse('<b> Hatalı Doğrulama Kod Girişi </b>')
    return render(request, 'uygulama/mail.html', form)


def main_page(request):  # main sayfa (tüm verification başarılı olursa yönlendirilecek sayfa)
    log = Log(user=data, email_ver=verification_data, ip_tables=ipaddress)
    log.save()
    return render(request, 'uygulama/page.html', {'name': name})


class SingedOutView(generic.TemplateView):  # logout sayfası
    template_name = 'uygulama/singed_out.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        logout(ipaddress)
        return render(request, self.template_name)


def send_mail(request):  # mail gönderme fonksiyonu
    global otp
    otp = send_simple_message(email)
    return redirect('uygulama:mail')


def give_permission(ipadress):  # internet izin verme fonksiyonu // iptables ayarları
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


def logout(ipadress):  # logout iptables iptal edilir
    remote_IP = ipadress
    subprocess.call(
        ["iptables", "-t", "nat", "-D", "PREROUTING", "-s", remote_IP, "-j", "ACCEPT"])  # iptables iptal edilir
    subprocess.call(["iptables", "-D", "FORWARD", "-s", remote_IP, "-j", "ACCEPT"])
    return redirect(request, 'templates/login.html')


# captive portal logout code
def firewall_logs():  # iptables logları alınır
    iptable_logs = subprocess.call(["iptables", "-L", "-n", "-v", "-x", "-t", "nat"])  # iptables logları alınır

    return iptable_logs
def get_ip():  # ip adresi alınır permission verilmesi için!
    hostname = socket.gethostname()  # hostname
    IPAddr = socket.gethostbyname(hostname)  # ip adresi
    return IPAddr


def sms(request):  # sms doğrulama sayfası (sms doğrulaması)/ simdilik mail ile doğrulama
    if request.method == 'POST':
        otp_verification = request.POST['otp']
        if otp == otp_verification:  # SMS API doğrulama
            ipaddress = get_ip()  # ip adresi
            give_permission(ipaddress)  # internet varsa session oluştur //oluşturulmadı sadece iptables ayarları var
            return redirect(request, 'uygulama:page')
        else:
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')
