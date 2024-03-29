# Generated by Django 4.2.3 on 2023-09-16 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_category_products_category_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='products.product', verbose_name='Products'),
        ),
    ]
