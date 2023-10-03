from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.views import status
from ..models import Client, Trainer
from ..serializers import ClientSerializer, TrainerSerializer

class ClientRelationTestCase(APITestCase):
    def setUp(self):
        self.user = Client.objects.create(username="test_client", 
                                          first_name="Adam", 
                                          last_name="Smith", password="123")
        self.trainer = Trainer.objects.create(username="test_trainer",
                                              first_name="John",
                                              last_name="Good", password="123")

    def test_create_client(self):
        client_url = reverse("clients-list")
        response = self.client.get(client_url)
        print(response.data)
        serializer_data = ClientSerializer(self.user).data
        print(serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #self.assertEqual(serializer_data, response.data, response.data)

    def test_create_trainer(self):
        trainer_url = reverse("trainers-list")
        response = self.client.get(trainer_url)
        print(response.data)
        serializer_data = TrainerSerializer(self.trainer).data
        print(serializer_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        #self.assertEqual(serializer_data, response.data)

