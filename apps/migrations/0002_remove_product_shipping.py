# Generated by Django 5.0.1 on 2024-03-27 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='shipping',
        ),
    ]