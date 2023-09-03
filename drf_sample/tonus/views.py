from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Client, Exercise, Trainer, ExerciseType
from .serializers import ClientSerializer, ExerciseSerializer, TrainerSerializer, ExercisePostSerializer, ExercisePutSerializer, \
        TrainerPostSerializer, TrainerPutSerializer

# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

# создали дополнительный маршрут к роутеру по пути clients/extype/
    @action(methods=['get'], detail=False)
    def extype(self, request):
        ex_type = ExerciseType.objects.all()
        return Response({'ex_type': [ex.title for ex in ex_type]})

class ExerciseViewSet(viewsets.ModelViewSet):

    queryset = Exercise.objects.all()
#    serializer_class = ExerciseSerializer


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExercisePostSerializer
        elif self.request.method == 'PUT':
            return ExercisePutSerializer
        return ExerciseSerializer

class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrainerPostSerializer
        elif self.request.method == 'PUT':
            return TrainerPutSerializer
        return TrainerSerializer

