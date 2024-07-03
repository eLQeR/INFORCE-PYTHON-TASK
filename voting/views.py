from datetime import datetime

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from cafe.models import CafeLunchMenu
from cafe.permissions import IsAdminOrReadOnly

from voting.models import Vote, ResultOfVoting
from voting.permissions import IsCreatorOrReadOnly
from voting.serializers import (
    VoteSerializer,
    ResultOfVotingDetailSerializer,
    ResultOfVotingListSerializer,
    VoteListSerializer,
)
from cafe.serializers import (
    CafeDetailSerializer,
    CafeLunchMenuDetailSerializer,
)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve own vote",
        description="User can get a detail info about own vote",
    ),
    create=extend_schema(
        summary="Create a cafe",
        description="User can create a vote.",
    ),
    update=extend_schema(
        summary="Update a own vote",
        description="User can update own vote.",
    ),
    partial_update=extend_schema(
        summary="Partial update a certain vote",
        description="User can make partial update own vote.",
    ),
    destroy=extend_schema(
        summary="Delete a vote",
        description="User can delete own vote.",
    ),
)
class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return self.queryset.filter(voter=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return VoteSerializer
        return VoteListSerializer

    def perform_create(self, serializer):
        serializer.save(voter=self.request.user)

    @extend_schema(
        summary="Get list of votes",
        description="User can get a list of votes",
        methods=["GET"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve a result of voting",
        description="User can get a certain result of voting.",
    ),
    update=extend_schema(
        summary="Update a certain result of voting",
        description="Admin can update a result of voting.",
    ),
    partial_update=extend_schema(
        summary="Partial update a certain result of voting",
        description="Admin can make partial update a result of voting.",
    ),
)
class ResultOfVotingView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ResultOfVoting.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    @extend_schema(
        summary="Get today's menu of cafe",
        description="Employee can get today's menu of cafe if voting is ended.",
        methods=["GET"],
    )
    @action(detail=False, methods=["GET"], url_path="get-today-cafe")
    def get_today_cafe(self, request):
        today = datetime.today().strftime("%a").upper()
        result = self.get_queryset()
        if result:
            cafe = result.first().result_cafe

            try:
                menu = CafeLunchMenu.objects.get(cafe=cafe, weekday=today)
            except CafeLunchMenu.DoesNotExist:
                return Response(CafeDetailSerializer(cafe).data, status=200)

            serializer = self.get_serializer(menu, many=False)
            return Response(serializer.data)
        return Response({"result": "It has not decided yet"}, status=200)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ResultOfVotingDetailSerializer
        if self.action == "get_today_cafe":
            return CafeLunchMenuDetailSerializer

        return ResultOfVotingListSerializer

    def get_queryset(self):
        queryset = self.queryset
        today = datetime.today()
        cafe = self.request.query_params.get("cafe", None)

        if cafe:
            queryset = queryset.filter(result_cafe__slug=cafe)

        if self.action == "get_today_cafe":
            queryset = self.queryset.filter(voting_date=today)

        return queryset

    @extend_schema(
        summary="Get list of results of voting",
        description="User can get a list of results of voting",
        methods=["GET"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
