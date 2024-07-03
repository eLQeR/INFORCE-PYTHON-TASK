from rest_framework.exceptions import ErrorDetail

from cafe.models import EstablishmentType, Cuisine, Cafe
from voting.models import Vote, ResultOfVoting
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User
from voting.serializers import VoteSerializer
from voting.tasks import select_the_winner_cafe

VOTING_ULR = "/api/voting/votes/"


class AuthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='Test-user',
            password='<PASSWORD>'
        )
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
            "cafe": self.cafe.pk,
            "voter": self.user.pk,
        }

        self.client.force_authenticate(user=self.user)

    def test_create_vote(self):
        response = self.client.post(VOTING_ULR, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vote = Vote.objects.last()
        self.assertEqual(response.data, VoteSerializer(vote, many=False).data)

    def test_create_two_vote_forbidden(self):
        self.client.post(VOTING_ULR, data=self.data)
        response = self.client.post(VOTING_ULR, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [
                ErrorDetail(
                    'The fields created_at, voter must make a unique set.', code="unique"
                )
            ]
        )

    def test_result_of_voting(self):
        user_1 = User.objects.create_superuser(
            username='Test-user-1',
            password='<PASSWORD>'
        )
        user_2 = User.objects.create_superuser(
            username='Test-user-2',
            password='<PASSWORD>'
        )
        Vote.objects.create(voter=user_1, cafe=self.cafe)
        Vote.objects.create(voter=user_2, cafe=self.cafe)
        Vote.objects.create(voter=self.user, cafe=self.bar)
        select_the_winner_cafe()
        response = self.client.get(f"/api/voting/results/get-today-cafe/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ResultOfVoting.objects.last().result_cafe, self.cafe)
        self.assertTrue(ResultOfVoting.objects.filter(result_cafe=self.cafe).exists())


class UnauthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='Test-user',
            password='<PASSWORD>'
        )
        self.type_cafe = EstablishmentType.objects.create(name='Cafe', slug='cafe')
        cuisine = Cuisine.objects.create(name='Ukrainian', slug='ukrainian')
        self.cafe = Cafe.objects.create(
            name='Cafe',
            description='cafe description',
            address='cafe address',
            slug='cafe-slug-2',
            cuisine=cuisine,
            type=self.type_cafe
        )
        self.vote = Vote.objects.create(voter=self.user, cafe=self.cafe)
        self.data = {
            "cafe": self.cafe.pk,
            "voter": self.user.pk,
        }

    def test_create_vote_forbidden(self):
        response = self.client.post(VOTING_ULR, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_vote_forbidden(self):
        response = self.client.put(f"{VOTING_ULR}1/", self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_vote_forbidden(self):
        response = self.client.delete(
            f"{VOTING_ULR}1/",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
