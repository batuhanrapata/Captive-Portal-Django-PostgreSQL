# Generated by Django 4.1.6 on 2023-02-14 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uygulama', '0008_log_email_ver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='sms',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='uygulama.sms'),
        ),
    ]
