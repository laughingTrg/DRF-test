# Generated by Django 4.2.4 on 2023-08-28 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tonus', '0006_alter_exercise_ex_type_alter_exercise_trainer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='ex_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='tonus.exercisetype', verbose_name='Вид тренировки'),
        ),
    ]
