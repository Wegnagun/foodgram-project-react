# Generated by Django 4.1.2 on 2022-10-28 21:35

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=7, samples=None, verbose_name='HEX-код цвета'),
        ),
    ]
