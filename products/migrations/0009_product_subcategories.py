# Generated by Django 5.0 on 2024-12-24 01:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.subcategories'),
        ),
    ]