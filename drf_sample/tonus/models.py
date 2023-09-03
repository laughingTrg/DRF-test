from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ExerciseType(models.Model):
    title = models.CharField(max_length=255)
    style = models.TextField(blank=False)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "Вид тренировки"
        verbose_name_plural = "Виды тренировок"

class Exercise(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    ex_type = models.ForeignKey("ExerciseType", related_name='exercises', on_delete=models.CASCADE, null=False, verbose_name="Вид тренировки")
    trainer = models.ForeignKey("Trainer", related_name='exercises', on_delete=models.PROTECT, null=False, verbose_name="Тренер")
    clients = models.ManyToManyField("Client", related_name='exercises', verbose_name="Клиенты")
    cli_num = models.IntegerField(default=10, blank=False, verbose_name="Количество человек")
    place = models.CharField(max_length=100, verbose_name="Зал")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.title} ({self.date}) {self.trainer.last_name}"

    def delete(self):
        self.deleted = True
        self.save()

    class Meta():
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"

class AdvUser(AbstractUser):

    is_activated = models.BooleanField(default=True)
    birthday_at = models.DateField(blank=True)

    class Meta(AbstractUser.Meta):
        pass

class Trainer(AdvUser):

    pass

    class Meta():
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"
        
    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} ({self.email})"

class Client(AdvUser):
   
    pass

    class Meta():
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name} ({self.email})"

