# Generated by Django 5.0 on 2024-12-23 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_subcategories_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategories',
            name='categories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='products.categories'),
        ),
    ]
