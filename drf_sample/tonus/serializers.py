from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Client, Exercise, Trainer

class ExercisePostSerializer(serializers.ModelSerializer):
    clients = serializers.HiddenField(default=None)

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'ex_type', 'trainer', 'clients', 'cli_num', 'place', )

class ExercisePutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'ex_type', 'trainer', 'clients', 'cli_num', 'place', )

class ExerciseSerializer(serializers.ModelSerializer):
    trainer = serializers.StringRelatedField()
    clients = serializers.StringRelatedField(many=True)


    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'ex_type', 'trainer', 'clients', 'cli_num', 'place', )

class ClientSerializer(serializers.ModelSerializer):
    exercises = serializers.StringRelatedField(many=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(ClientSerializer, self).create(validated_data)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'exercises', 'birthday_at', 'username')

class TrainerSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'exercises', 'birthday_at', 'username')

class TrainerPostSerializer(serializers.ModelSerializer):
    exercises = serializers.HiddenField(default=[])

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(TrainerPostSerializer, self).create(validated_data)

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'exercises', 'birthday_at', 'username')

class TrainerPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'exercises', 'birthday_at', 'username')
