# Generated by Django 4.1.3 on 2023-04-15 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonDRF", "0022_alter_cart_user_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="user_token",
        ),
    ]
