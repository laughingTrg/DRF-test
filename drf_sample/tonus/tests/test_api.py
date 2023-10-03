from django.db.models import Avg, Case, Count, When
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status
from ..models import Client, ClientExerciseRelation, Exercise, ExerciseType, Trainer
from ..serializers import ClientSerializer, ExerciseSerializer, ExerciseTypeSerializer, TrainerClientField, TrainerSerializer


class ExerciseTestCase(APITestCase):
    def setUp(self):
        self.user = Client.objects.create(username="test_client", 
                                          first_name="Adam", 
                                          last_name="Smith", password="123")
        self.trainer = Trainer.objects.create(username="test_trainer",
                                              first_name="John",
                                              last_name="Good", password="123")
        self.ex_type = ExerciseType.objects.create(title="Cardio")

    def test_ok(self):
        exercise_1 = Exercise.objects.create(title="Jumping", 
                                             date="2023-09-06",
                                             time="18:15:00",
                                             ex_type=self.ex_type, 
                                             trainer=self.trainer,
                                             cli_num=10)

        data2 = ExerciseSerializer(exercise_1).data
        print(data2)
        data = ExerciseTypeSerializer(self.ex_type).data

        expected_data = {
            'id': self.ex_type.id,
            'title': 'Cardio',
            'style': '',
            'description': '',
        }
        expected_data2 = {
            'id': exercise_1.id,
            'title': 'Jumping',
            'date': '2023-09-06',
            'time': '18:15:00',
            'ex_type': 'Cardio : ',
            'trainer': 'John Good : ',
            'clients': [],
            'cli_num': 10,
            'place': '',
            'likes': 0,
            'rating': None,
            'annotated_likes': 0
        }
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_data2, data2)


class ExerciseAnotateLikesTestCase(APITestCase):
    def setUp(self):
        self.user1 = Client.objects.create(username="test_client1", 
                                          first_name="Adam", 
                                          last_name="Smith", password="123")
        self.user2 = Client.objects.create(username="test_client2", 
                                          first_name="Adam", 
                                          last_name="Smith", password="123")
        self.user3 = Client.objects.create(username="test_client3", 
                                          first_name="Adam", 
                                          last_name="Smith", password="123")
        self.trainer = Trainer.objects.create(username="test_trainer",
                                              first_name="John",
                                              last_name="Good", password="123")
        self.ex_type = ExerciseType.objects.create(title="Cardio")

    def test_ok(self):
        exercise_1 = Exercise.objects.create(title="Jumping", 
                                             date="2023-09-06",
                                             time="18:15:00",
                                             ex_type=self.ex_type, 
                                             trainer=self.trainer,
                                             cli_num=10)
        exercise_2 = Exercise.objects.create(title="Jumping2", 
                                             date="2023-09-06",
                                             time="18:15:00",
                                             ex_type=self.ex_type, 
                                             trainer=self.trainer,
                                             cli_num=10)

        ClientExerciseRelation.objects.create(client=self.user1, 
                                              exercise=exercise_1,
                                              like=True,
                                              rate=4)
        ClientExerciseRelation.objects.create(client=self.user2, 
                                              exercise=exercise_1,
                                              like=True,
                                              rate=5)
        ClientExerciseRelation.objects.create(client=self.user3, 
                                              exercise=exercise_1,
                                              like=True)

        ClientExerciseRelation.objects.create(client=self.user1, 
                                              exercise=exercise_2,
                                              like=True,
                                              rate=3)
        ClientExerciseRelation.objects.create(client=self.user2, 
                                              exercise=exercise_2,
                                              like=True,
                                              rate=4)
        ClientExerciseRelation.objects.create(client=self.user3, 
                                              exercise=exercise_2,
                                              like=False)
        
        exercises = Exercise.objects.all().annotate(
            annotated_likes=Count(Case(When(clientexerciserelation__like=True,
                                            then=1))),
            rating=Avg("clientexerciserelation__rate"))

        data = ExerciseSerializer(exercises, many=True).data

        expected_data = [{
            'id': exercise_1.id,
            'title': 'Jumping',
            'date': '2023-09-06',
            'time': '18:15:00',
            'ex_type': 'Cardio : ',
            'trainer': 'John Good : ',
            'clients': [],
            'cli_num': 10,
            'place': '',
            'likes': 3,
            'annotated_likes': 3,
            'rating': '4.50'
        },{
            'id': exercise_2.id,
            'title': 'Jumping2',
            'date': '2023-09-06',
            'time': '18:15:00',
            'ex_type': 'Cardio : ',
            'trainer': 'John Good : ',
            'clients': [],
            'cli_num': 10,
            'place': '',
            'likes': 2,
            'annotated_likes': 2,
            'rating': '3.50'
        }]

        self.assertEqual(expected_data, data)

