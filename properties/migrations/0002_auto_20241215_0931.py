# Generated by Django 3.2 on 2024-12-15 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='title',
        ),
        migrations.AddField(
            model_name='property',
            name='bathroom',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='property',
            name='bedroom',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='property',
            name='electricity',
            field=models.PositiveSmallIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable'), ('sold', 'Sold'), ('rented', 'Rented')], max_length=50),
        ),
    ]