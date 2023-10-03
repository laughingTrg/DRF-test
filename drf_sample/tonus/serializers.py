from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Client, ClientExerciseRelation, Exercise, Trainer, ExerciseType


class ExerciseTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExerciseType
        exclude = ('is_published', )


class ExercisePostSerializer(serializers.ModelSerializer):
    clients = serializers.HiddenField(default=[])

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'time', 'ex_type',
                  'trainer', 'clients', 'cli_num', 'place', )


class ExercisePutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'time', 'ex_type',
                  'trainer', 'clients', 'cli_num', 'place', )


class ExerciseTypeField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.title} : {value.style}'


class TrainerClientField(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.first_name} {value.last_name} : {value.email}'


class ExerciseSerializer(serializers.ModelSerializer):
    ex_type = ExerciseTypeField(read_only=True)
    trainer = TrainerClientField(read_only=True)
    clients = TrainerClientField(many=True, allow_null=True, read_only=True)
    likes = serializers.SerializerMethodField()
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(decimal_places=2, max_digits=3)

    class Meta:
        model = Exercise
        fields = ('id', 'title', 'date', 'time', 'ex_type',
                  'trainer', 'clients', 'cli_num', 'place', 'likes', 
                  'annotated_likes', 'rating')

    def get_likes(self, instance):
        return ClientExerciseRelation.objects.filter(exercise=instance, \
                like=True).count()


class ExerciseField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.title} ({value.date} {value.time}) Тренер: {value.trainer.last_name} {value.trainer.first_name}"


class ClientSerializer(serializers.ModelSerializer):
    exercises = ExerciseField(many=True, read_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(ClientSerializer, self).create(validated_data)

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'exercises', 'birthday_at', 'username')


class TrainerSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'exercises', 'birthday_at', 'username')


class TrainerPostSerializer(serializers.ModelSerializer):
    exercises = serializers.HiddenField(default=[])

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(TrainerPostSerializer, self).create(validated_data)

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'exercises', 'birthday_at', 'username')


class TrainerPutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password', 'exercises', 'birthday_at', 'username')


class ClientExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientExerciseRelation
        fields = ("exercise", "like", "rate", )
