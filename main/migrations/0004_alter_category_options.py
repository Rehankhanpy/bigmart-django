# Generated by Django 4.2.6 on 2023-10-30 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
    ]
