from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from cafe.models import Cafe, CafeLunchMenu, EstablishmentType, Cuisine
from cafe.serializers import CafeListSerializer, CafeDetailSerializer


CAFE_URL = "/api/catalog/cafes/"

class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='user', password='<PASSWORD>')
        self.client.force_authenticate(user=self.user)
        self.type_bar = EstablishmentType.objects.create(name='Bar', slug='bar')
        self.type_cafe = EstablishmentType.objects.create(name='Cafe', slug='cafe')
        cuisine = Cuisine.objects.create(name='Ukrainian', slug='ukrainian')
        self.bar = Cafe.objects.create(
            name='Bar',
            description='Bar description',
            address='Bar address',
            slug='bar-slug-1',
            cuisine=cuisine,
            type=self.type_bar
        )
        self.cafe = Cafe.objects.create(
            name='Cafe',
            description='cafe description',
            address='cafe address',
            slug='cafe-slug-2',
            cuisine=cuisine,
            type=self.type_cafe
        )
        self.data = {
            "name": "Test Bar",
            "description": "Test description",
            "address": "test address",
            "slug": "test-bar",
            "cuisine": cuisine.pk,
            "type": self.type_bar.pk,
        }

    def test_get_cafes(self):
        response = self.client.get(CAFE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cafes = Cafe.objects.all()
        self.assertEqual(len(response.data["results"]), cafes.count())
        self.assertEqual(
            response.data["results"],
            (CafeListSerializer(cafes, many=True).data)
        )

    def test_filtered_cafes(self):
        response = self.client.get(f"{CAFE_URL}?types={self.type_bar.pk}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"],
            CafeListSerializer([self.bar], many=True).data
        )

    def test_retrieve_cafe(self):
        response = self.client.get(f"{CAFE_URL}{self.cafe.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            CafeDetailSerializer(self.cafe, many=False).data
        )

    def test_create_cafe_forbidden(self):
        response = self.client.post(
            CAFE_URL,
            self.data,
        )
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertRaises(ObjectDoesNotExist, Cafe.objects.get, name="Test Bar")

    def test_update_cafe_forbidden(self):
        response = self.client.put(
            "/api/catalog/cafes/1/",
            self.data,
        )
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        self.assertRaises(ObjectDoesNotExist, Cafe.objects.get, name="Test Bar")

    def test_delete_cafe_forbidden(self):
        response = self.client.delete(
            f"{CAFE_URL}1/",
        )
        db_airport_id_1 = Cafe.objects.filter(pk=1)

        self.assertEqual(db_airport_id_1.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invalid_airport(self):
        response = self.client.get(F"{CAFE_URL}1001/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#
# class AdminApiTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         user = User.objects.create_superuser(username='admin_user', password='<PASSWORD>')
#         self.client.force_authenticate(user=user)
#         self.data = {
#                 "name": "Scarlett",
#                 "closest_big_city": "New York",
#             }
#
#         Airport.objects.create(name="Georginia", closest_big_city="Milan")
#         self.airport = Airport.objects.create(name="Kean", closest_big_city="Paris")
#
#     def test_create_airport(self):
#         response = self.client.post(
#             "/api/airlines/airports/",
#             self.data,
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["closest_big_city"], "New York")
#         self.assertEqual(Airport.objects.count(), 3)
#
#     def test_update_airport(self):
#         response = self.client.put(
#             "/api/airlines/airports/1/",
#             self.data,
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["closest_big_city"], "New York")
#         self.assertEqual(Airport.objects.count(), 2)
#         self.assertEqual(Airport.objects.get(pk=1).name, "Scarlett")
#
#
#     def test_delete_airport(self):
#         response = self.client.delete(
#             "/api/airlines/airports/1/",
#         )
#         db_airport_id_1 = Airport.objects.filter(pk=1)
#
#         self.assertEqual(db_airport_id_1.count(), 0)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_delete_invalid_airport(self):
#         response = self.client.delete(
#             "/api/airlines/airports/1001/",
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
