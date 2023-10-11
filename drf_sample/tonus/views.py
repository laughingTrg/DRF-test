from django.shortcuts import render
from django.db.models import Case, When, Count, Avg
from rest_framework import generics, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, \
    RetrieveModelMixin
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .filters import ExerciseFilter, TrainerFilter

from .permission import ReadOnly
from .models import Client, ClientExerciseRelation, Exercise, Trainer, \
    ExerciseType
from .serializers import ClientExerciseSerializer, ClientSerializer, \
    ExerciseSerializer, ExerciseTypeSerializer, \
    TrainerSerializer, ExercisePostSerializer, ExercisePutSerializer, \
    TrainerPostSerializer, TrainerPutSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().prefetch_related("exercises")
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAdminUser | ReadOnly, )

# создали дополнительный маршрут к роутеру по пути clients/extype/
    @action(methods=['get'], detail=False)
    def extype(self, request):
        ex_type = ExerciseType.objects.all()
        return Response({'ex_type': [ex.title for ex in ex_type]})


class ExerciseTypeViewSet(viewsets.ModelViewSet):
    queryset = ExerciseType.objects.all()
    serializer_class = ExerciseTypeSerializer
    permission_classes = (permissions.IsAdminUser, )


class ExerciseViewSet(viewsets.ModelViewSet):

    queryset = Exercise.objects.all().select_related("ex_type").\
        select_related("trainer").prefetch_related("clients").annotate(
        annotated_likes=Count(Case(When(clientexerciserelation__like=True,
                                        then=1))),
        rating=Avg("clientexerciserelation__rate"))
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExerciseFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExercisePostSerializer
        elif self.request.method == 'PUT':
            return ExercisePutSerializer
        return ExerciseSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = (permissions.IsAdminUser | ReadOnly, )
    filterset_class = TrainerFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrainerPostSerializer
        elif self.request.method == 'PUT':
            return TrainerPutSerializer
        return TrainerSerializer


class ClientExerciseRelationView(UpdateModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ClientExerciseRelation.objects.all()
    serializer_class = ClientExerciseSerializer
    lookup_field = "exercise"

    def get_object(self):
        obj, _ = ClientExerciseRelation.objects.get_or_create(
            user=self.request.user,
            exercise=self.kwargs['exercise'])
        return obj
