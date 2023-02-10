from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'tc_no', 'birth_date', 'tel_no', 'confirmation', 'email', 'timestamp')
    search_fields = ('name',)
    pass


@admin.register(Sms)
class SmsAdmin(admin.ModelAdmin):
    list_display = ('sms_code', 'confirmation', 'timestamp')
    pass


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'sms', 'timestamp', 'ip_tables')
    search_fields = ('ip_tables',)
    list_filter = ('timestamp',)
    pass
