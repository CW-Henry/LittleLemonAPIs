# Generated by Django 4.1.3 on 2023-04-15 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0011_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='menuitem_test',
        ),
    ]