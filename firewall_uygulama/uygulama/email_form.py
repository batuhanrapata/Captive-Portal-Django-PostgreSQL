from django import forms


class MailForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, widget=forms.TextInput(attrs={'placeholder': 'OTP'}),
                          error_messages={'required': 'Lütfen OTP giriniz.'}, help_text='OTP giriniz.')

    class Meta:
        fields = ['otp']
