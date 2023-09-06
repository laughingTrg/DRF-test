# Generated by Django 4.2.4 on 2023-08-28 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tonus', '0005_alter_advuser_birthday_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='ex_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='tonus.exercisetype', verbose_name='Вид тренировки'),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exercises', to='tonus.trainer', verbose_name='Тренер'),
        ),
    ]
