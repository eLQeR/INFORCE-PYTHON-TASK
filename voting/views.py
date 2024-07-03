from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cafe.models import Cafe, CafeLunchMenu
from cafe.permissions import IsAdminOrReadOnly

from voting.models import Vote, ResultOfVoting
from voting.permissions import IsCreatorOrReadOnly
from voting.serializers import VoteSerializer
from voting.tasks import select_the_winner_cafe
from cafe.serializers import (
    CafeDetailSerializer,
    CafeLunchMenuListSerializer,
    CafeLunchMenuDetailSerializer,
    LunchDishSerializer,
)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(voter=self.request.user)


class ResultOfVotingView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = ResultOfVoting.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_today_cafe(self, request):
        today = datetime.today().strftime("%a")
        # select_the_winner_cafe()
        result = self.get_queryset()
        if result:
            cafe = result.first().result_cafe

            try:
                menu = CafeLunchMenu.objects.get(cafe=cafe, weekday=today)
            except CafeLunchMenu.DoesNotExist:
                return Response(CafeDetailSerializer(cafe).data, status=200)

            serializer = self.get_serializer(menu, many=False)
            return Response(serializer.data, status=200)
        return Response({"result": "It hasn't decided yet"}, status=200)

    def get_serializer_class(self):
        if self.action == 'list':
            return CafeLunchMenuListSerializer
        if self.action == 'retrieve':
            return CafeLunchMenuDetailSerializer
        return CafeLunchMenuListSerializer


    def get_queryset(self):
        queryset = self.queryset
        today = datetime.today()
        cafe = self.request.query_params.get("cafe", None)

        if cafe:
            queryset = queryset.filter(cafe__slug=cafe)

        if self.action == "get_today_cafe":
            queryset = self.queryset.filter(voting_date=today)

        return queryset
