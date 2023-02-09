from django.db import models


# Create your models here.
class User(models.Model):  # User model
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    tc_no = models.CharField(max_length=11)
    birth_date = models.CharField(max_length=4)
    tel_no = models.CharField(max_length=10)
    confirmation = models.BooleanField()
    email = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tc_no


class Sms(models.Model):  # Sms model
    sms_code = models.CharField(max_length=8)
    confirmation = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sms_code


class Log(models.Model):  # Log model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sms = models.ForeignKey(Sms, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_tables = models.CharField(max_length=40, default='iptables ayarları')

    def __str__(self):
        return self.user
