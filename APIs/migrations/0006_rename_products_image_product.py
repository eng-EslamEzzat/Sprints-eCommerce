# Generated by Django 4.0.4 on 2022-06-09 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APIs', '0005_alter_image_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='products',
            new_name='product',
        ),
    ]
