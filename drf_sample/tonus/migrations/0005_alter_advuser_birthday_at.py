# Generated by Django 4.2.4 on 2023-08-28 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tonus', '0004_alter_client_options_alter_exercise_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='birthday_at',
            field=models.DateField(blank=True),
        ),
    ]
