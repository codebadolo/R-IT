# Generated by Django 5.0 on 2024-12-27 00:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_subcategories'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributevalue',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
