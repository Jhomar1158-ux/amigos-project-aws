# Generated by Django 3.2.9 on 2021-12-08 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amigos',
            name='name',
        ),
    ]