# Generated by Django 3.2.16 on 2025-01-03 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20250102_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Загрузите изображение.', null=True, upload_to='posts/', verbose_name='Изображение'),
        ),
    ]