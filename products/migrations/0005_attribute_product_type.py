# Generated by Django 5.0 on 2024-12-22 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_attributes_producttypeattribute_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='product_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='products.producttype'),
        ),
    ]
