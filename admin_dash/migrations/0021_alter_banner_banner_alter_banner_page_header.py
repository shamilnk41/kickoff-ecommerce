# Generated by Django 4.2.4 on 2023-11-18 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dash', '0020_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='banner/img'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='page_header',
            field=models.ImageField(blank=True, null=True, upload_to='page_header/img'),
        ),
    ]
