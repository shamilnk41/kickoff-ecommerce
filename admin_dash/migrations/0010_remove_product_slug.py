# Generated by Django 4.2.6 on 2023-10-19 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dash', '0009_remove_product_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
