# Generated by Django 4.2.6 on 2023-10-20 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dash', '0010_remove_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
