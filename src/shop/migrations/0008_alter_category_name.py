# Generated by Django 4.1.7 on 2023-02-22 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_category_alter_productimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
