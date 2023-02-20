from django.db import models



# Create your models here.
class User(models.Model):  # User model
    name = models.CharField(max_length=40,  default="null")
    surname = models.CharField(max_length=40,  default="null")
    tc_no = models.CharField(max_length=11,  default="null")
    birth_date = models.CharField(max_length=4, default="null")
    tel_no = models.CharField(max_length=11, default="null")
    confirmation = models.BooleanField()
    email = models.CharField(max_length=40, default="null")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tc_no


class Sms(models.Model):  # Sms model
    sms_code = models.CharField(max_length=8, default="null")
    confirmation = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Sms'

    def __str__(self):
        return self.sms_code


class email_verification(models.Model):  # Email model
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="null")
    email_code = models.CharField(max_length=6)
    confirmation = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Email'

    def __str__(self):
        return self.email_code


class Log(models.Model):  # Log model
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="null")
    sms = models.ForeignKey(Sms, on_delete=models.CASCADE, default="null")
    email_ver = models.ForeignKey(email_verification, on_delete=models.CASCADE, default="null")
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_tables = models.CharField(max_length=40, default='null')

    class Meta:
        verbose_name_plural = 'Log'

    def __str__(self):
        return self.ip_tables
