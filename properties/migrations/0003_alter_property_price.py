# Generated by Django 3.2 on 2024-12-15 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20241215_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.CharField(max_length=10),
        ),
    ]