from django.contrib import admin
from .models import Client, Exercise, ExerciseType, Trainer, \
        ClientExerciseRelation

# Register your models here.
admin.site.register(Trainer)
admin.site.register(Client)
admin.site.register(ExerciseType)
admin.site.register(Exercise)
admin.site.register(ClientExerciseRelation)
