# Generated by Django 4.0.2 on 2022-02-21 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plates', '0007_repository_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='desc',
            field=models.TextField(null=True),
        ),
    ]
