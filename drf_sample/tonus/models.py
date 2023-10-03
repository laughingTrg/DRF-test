from django.db import models
from django.contrib.auth.models import AbstractUser


class ExerciseType(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    style = models.TextField(blank=False, verbose_name="Вид тренировки")
    description = models.TextField(blank=True, \
            verbose_name="Описание тренировки")
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "Вид тренировки"
        verbose_name_plural = "Виды тренировок"


class Exercise(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    date = models.DateField(verbose_name="Дата проведения занятия")
    time = models.TimeField(verbose_name="Время проведения")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    ex_type = models.ForeignKey("ExerciseType", related_name='exercises',
                                on_delete=models.CASCADE, null=False,
                                verbose_name="Вид тренировки")
    trainer = models.ForeignKey("Trainer", related_name='exercises',
                                on_delete=models.PROTECT, null=True,
                                verbose_name="Тренер")
    clients = models.ManyToManyField(
        "Client", related_name='exercises', verbose_name="Клиенты", 
        blank=True)
    cli_num = models.IntegerField(
        default=10, blank=False, verbose_name="Количество человек")
    place = models.CharField(max_length=100, verbose_name="Зал")
    deleted = models.BooleanField(default=False, \
            verbose_name="Тренировка закончилась")
    likers = models.ManyToManyField("Client", through="ClientExerciseRelation")

    def __str__(self):
        return f"{self.pk} {self.title} ({self.date} {self.time})" \
                f" {self.trainer.last_name}"

    def delete(self):
        self.deleted = True
        self.save()

    class Meta():
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ('date', 'time',)


class AdvUser(AbstractUser):

    is_activated = models.BooleanField(default=True)
    birthday_at = models.DateField(blank=True, null=True)

    class Meta(AbstractUser.Meta):
        pass


class Trainer(AdvUser):

    pass

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} ({self.email})"


class Client(AdvUser):

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} ({self.email})"


class ClientExerciseRelation(models.Model):
    RATE_CHOISES = (
            (1, 'Больше не приду'),
            (2, 'Не очень'),
            (3, 'Нормально'),
            (4, 'Хорошо'),
            (5, 'Отлично')
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, \
            verbose_name="Клиент")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, \
            verbose_name="Тренировка")
    like = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOISES, null=True)

    def __str__(self):
        return f"{self.client.last_name} - {self.exercise.title} ({self.rate})"

    class Meta:
        verbose_name = "Лайки"
        verbose_name_plural = "Лайки"
