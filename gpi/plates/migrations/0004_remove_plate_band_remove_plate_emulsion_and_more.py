# Generated by Django 4.0.2 on 2022-02-11 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plates', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plate',
            name='band',
        ),
        migrations.RemoveField(
            model_name='plate',
            name='emulsion',
        ),
        migrations.RemoveField(
            model_name='plate',
            name='filt',
        ),
        migrations.RemoveField(
            model_name='telescope',
            name='obs',
        ),
    ]