# Generated by Django 5.0 on 2024-12-21 23:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_attribute_productbrand_producttype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='products.attribute'),
        ),
        migrations.AddField(
            model_name='producttypeattribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
