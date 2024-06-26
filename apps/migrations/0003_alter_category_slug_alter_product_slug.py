# Generated by Django 5.0.1 on 2024-03-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_remove_product_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
