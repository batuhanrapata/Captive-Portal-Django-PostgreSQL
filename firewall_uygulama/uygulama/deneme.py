from firewall_uygulama.uygulama.myFunctions.kps_api import kps

print(kps("batuhan", "rapata", "37585646262", "1999"))








"""yedekler"""
"""def login_page(request):  # login sayfası (kps doğrulaması)
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

    return render(request, 'uygulama/login.html', form)"""



"""def mail(request):
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
            request.session['logged_in'] = True
            give_permission(ipaddress)  # internet varsa session oluştur //oluşturulmadı sadece iptables ayarları var
            return redirect('uygulama:page')
        else:
            return HttpResponse('<b> Hatalı Doğrulama Kod Girişi </b>')
    return render(request, 'uygulama/mail.html', form)"""



"""def main_page(request):  # main sayfa (tüm verification başarılı olursa yönlendirilecek sayfa)
    if request.session.get('logged_in'):
        log = Log(user=data, email_ver=verification_data, ip_tables=ipaddress)
        log.save()
        return render(request, 'uygulama/page.html', {'name': name})
    else:
        return redirect('uygulama:login')"""

"""
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
"""
