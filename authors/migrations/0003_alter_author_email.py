# Generated by Django 5.1.2 on 2024-10-13 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_author_email_author_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
