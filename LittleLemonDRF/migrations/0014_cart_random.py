# Generated by Django 4.1.3 on 2023-04-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonDRF", "0013_cart_user_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="random",
            field=models.TextField(default="dwdwdwdw"),
        ),
    ]
