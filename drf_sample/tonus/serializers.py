from rest_framework import serializers
from .models import Client, Exercise, Trainer


class ExerciseSerializer(serializers.ModelSerializer):
    trainer = serializers.StringRelatedField()
    clients = serializers.StringRelatedField(many=True)

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'ex_type', 'trainer', 'clients', 'cli_num', 'place', )

class ClientSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email', 'exercises')

class TrainerSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email', 'exercises')
