# Generated by Django 4.1.4 on 2023-07-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_available',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]