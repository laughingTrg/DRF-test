from django.contrib import admin
from .models import  Client, Exercise, ExerciseType, Trainer

# Register your models here.
admin.site.register(Trainer)
admin.site.register(Client)
admin.site.register(ExerciseType)
admin.site.register(Exercise)
