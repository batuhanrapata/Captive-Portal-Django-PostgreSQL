from django.http import request
from django.shortcuts import render, redirect
from .models import User, Sms, Log, email_verification
from .sms_api import *
from .kps_api import *
from .mailgun_api import send_simple_message
from django.views import generic
from .login_form import LoginForm
from .email_form import MailForm
from django.http import HttpResponse
from django.views import View
from dotenv import load_dotenv
from .user_settings import *

load_dotenv()

PORT = os.environ.get("PORT")
IFACE = os.environ.get("IFACE")
IP_ADDRESS = os.environ.get("IP_ADDRESS")


class login_view(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'uygulama/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            global name, surname, tc_no, birth_date, tel_no, email, confirmation, data
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
        return render(request, 'uygulama/login.html', {'form': form})


class mail_view(View):
    def get(self, request):
        form = MailForm()
        return render(request, 'uygulama/mail.html', {'form': form})

    def post(self, request):
        form = MailForm(request.POST)
        if form.is_valid():
            otp_verification = request.POST['otp']
            if otp == otp_verification:  # SMS API doğrulama
                global verification_data
                verification_data = email_verification(user=data, email_code=otp, confirmation=True)
                verification_data.save()  # email doğrulama kodu doğruysa veritabanına kaydet
                global ipaddress
                ipaddress = get_ip()
                request.session['logged_in'] = True
                give_permission(
                    ipaddress)  # internet varsa session oluştur //oluşturulmadı sadece iptables ayarları var
                return redirect('uygulama:page')
            else:
                return HttpResponse('<b> Hatalı Doğrulama Kod Girişi </b>')
        return render(request, 'uygulama/mail.html', {'form': form})


class main_page_view(generic.TemplateView):  # main sayfa (tüm verification başarılı olursa yönlendirilecek sayfa)
    template_name = 'uygulama/page.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('logged_in'):
            log = Log(user=data, email_ver=verification_data, ip_tables=ipaddress)
            log.save()
            return render(request, self.template_name, {'name': name})
        else:
            return redirect('uygulama:login')


class SingedOutView(generic.TemplateView):  # logout sayfası
    template_name = 'uygulama/singed_out.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        request.session['logged_in'] = False  # session silinir
        logout(ipaddress)
        return render(request, self.template_name)


def send_mail(request):  # SEND AGAIN MAIL
    global otp
    otp = send_simple_message(email)
    return redirect('uygulama:mail')



#sendgrid twilio api çöp olduğu için mailgun api kullanıldı
def sms(request):
    if request.method == 'POST':
        otp_verification = request.POST['otp']
        if otp == otp_verification:
            ipaddress = get_ip()
            give_permission(ipaddress)
            return redirect(request, 'uygulama:page')
        else:
            return 'Hatalı Kod Girişi'
    return render(request, 'uygulama/sms.html')
