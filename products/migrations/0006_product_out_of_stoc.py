# Generated by Django 4.2.5 on 2023-10-01 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_placedeoderitem_placed_oder'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='out_of_stoc',
            field=models.BooleanField(default=False),
        ),
    ]
