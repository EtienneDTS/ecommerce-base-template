# Generated by Django 4.1.7 on 2023-03-03 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_cart_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='selected',
            field=models.BooleanField(default=True),
        ),
    ]