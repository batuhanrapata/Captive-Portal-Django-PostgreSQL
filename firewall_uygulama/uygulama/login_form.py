from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Adınız'}),
                           error_messages={'required': 'Lütfen adınızı giriniz.'}, help_text='Adınızı giriniz.')
    surname = forms.CharField(max_length=100, required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Soyadınız'}),
                              error_messages={'required': 'Lütfen soyadınızı giriniz.'},
                              help_text='Soyadınızı giriniz.')
    tc_no = forms.CharField(max_length=11, required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'T.C. Kimlik Numaranız'}),
                            error_messages={'required': 'Lütfen T.C. Kimlik Numaranızı giriniz.'},
                            help_text='T.C. Kimlik Numaranızı giriniz.')
    birth_date = forms.CharField(max_length=4, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Doğum Tarihiniz'}),
                                 error_messages={'required': 'Lütfen doğum tarihinizi giriniz.'},
                                 help_text='Doğum tarihinizi giriniz. (Örn: 1999)')
    tel_no = forms.CharField(max_length=11, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Telefon Numaranız'}),
                             error_messages={'required': 'Lütfen telefon numaranızı giriniz.'},
                             help_text='Telefon numaranızı giriniz. (Örn: 0532 555 55 55)')
    email = forms.EmailField(max_length=100, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'E-Posta Adresiniz'}),
                             error_messages={'required': 'Lütfen e-posta adresinizi giriniz.'},
                             help_text='E-posta adresinizi giriniz. (Örn:ornek@example.com)')

    class Meta:
        fields = ['name', 'surname', 'tc_no', 'birth_date', 'tel_no', 'email']
