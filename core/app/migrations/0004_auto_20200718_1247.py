# Generated by Django 3.0.7 on 2020-07-18 07:17

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200718_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
    ]
