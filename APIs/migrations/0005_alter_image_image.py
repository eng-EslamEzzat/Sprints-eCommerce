# Generated by Django 4.0.4 on 2022-06-09 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0004_remove_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
