# Generated by Django 4.2.5 on 2023-09-20 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20230920_1950'),
        ('home', '0002_remove_categories_slug_remove_industry_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayHotProductInCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media')),
                ('title', models.CharField(max_length=200)),
                ('product_url', models.CharField(max_length=200)),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.categories')),
            ],
        ),
        migrations.RemoveField(
            model_name='subcategories',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.DeleteModel(
            name='Industry',
        ),
        migrations.DeleteModel(
            name='SubCategories',
        ),
    ]