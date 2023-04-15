# Generated by Django 4.1.3 on 2023-04-15 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonDRF', '0009_remove_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='menuitem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='LittleLemonDRF.menuitem'),
        ),
    ]