# Generated by Django 4.1.6 on 2023-02-14 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uygulama', '0009_alter_log_sms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email_verification',
            options={'verbose_name_plural': 'Email'},
        ),
        migrations.AlterModelOptions(
            name='log',
            options={'verbose_name_plural': 'Log'},
        ),
        migrations.AlterModelOptions(
            name='sms',
            options={'verbose_name_plural': 'Sms'},
        ),
    ]
