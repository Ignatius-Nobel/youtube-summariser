# Generated by Django 5.1 on 2024-09-03 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videodetail',
            name='blog',
            field=models.TextField(default='null'),
        ),
    ]
