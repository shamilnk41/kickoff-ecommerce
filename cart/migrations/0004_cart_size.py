# Generated by Django 4.2.6 on 2023-11-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
