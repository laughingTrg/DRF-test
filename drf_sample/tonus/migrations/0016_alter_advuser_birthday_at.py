# Generated by Django 4.2.4 on 2023-10-02 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tonus', '0015_alter_clientexerciserelation_options_exercise_likers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='birthday_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
