# Generated by Django 4.1.7 on 2023-03-04 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_cartproduct_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_product',
            field=models.IntegerField(default=0),
        ),
    ]