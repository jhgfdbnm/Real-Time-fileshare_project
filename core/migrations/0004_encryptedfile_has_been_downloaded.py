# Generated by Django 4.2.23 on 2025-06-23 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_encryptedfile_expires_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='encryptedfile',
            name='has_been_downloaded',
            field=models.BooleanField(default=False),
        ),
    ]
