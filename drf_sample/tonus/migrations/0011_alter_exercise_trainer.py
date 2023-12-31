# Generated by Django 4.2.4 on 2023-09-05 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tonus', '0010_alter_exercise_clients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='exercises', to='tonus.trainer', verbose_name='Тренер'),
        ),
    ]
