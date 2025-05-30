# Generated by Django 4.2.20 on 2025-04-23 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("good", "0002_city_region"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="category",
            index=models.Index(
                fields=["parent"], name="good_catego_parent__c19bc5_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="category",
            index=models.Index(fields=["slug"], name="good_catego_slug_3914e5_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["city", "category"], name="good_city_id_06f235_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["on_stock"], name="good_on_stoc_4d85e7_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["slug", "city", "category"], name="good_slug_15f963_idx"
            ),
        ),
    ]
