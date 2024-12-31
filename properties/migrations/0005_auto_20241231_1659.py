# Generated by Django 3.2 on 2024-12-31 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='parlor_image',
            field=models.ImageField(blank=True, upload_to='elbis/parlor_image/'),
        ),
        migrations.AlterField(
            model_name='property',
            name='bathroom_image',
            field=models.ImageField(blank=True, upload_to='elbis/bathroom_images/'),
        ),
        migrations.AlterField(
            model_name='property',
            name='bedroom_image',
            field=models.ImageField(blank=True, upload_to='elbis/bedroom_images/'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(choices=[('1 Room', '1 Room'), ('Self Contain', 'Self Contain'), ('Flat', 'Flat'), ('Duplex', 'Duplex'), ('Bungalow', 'Bungalow')], max_length=50),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')], max_length=50),
        ),
    ]