from django_filters import rest_framework as filters

from .models import Exercise, Trainer


class ExerciseFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Exercise
        fields = ('title', 'trainer', )


class TrainerFilter(filters.FilterSet):

    class Meta:
        model = Trainer
        fields = ('first_name', 'last_name', 'exercises', )
