from datetime import datetime

from django.core.exceptions import FieldError
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination

from cafe.models import Cafe, CafeLunchMenu
from cafe.permissions import IsAdminOrReadOnly
from cafe.serializers import (
    CafeSerializer,
    CafeListSerializer,
    CafeDetailSerializer,
    CafeLunchMenuListSerializer,
    CafeLunchMenuDetailSerializer,
    LunchDishSerializer,
)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve a certain cafe",
        description="User can get a detail info about cafe.",
    ),
    create=extend_schema(
        summary="Create a cafe",
        description="Admin can create a cafe.",
    ),
    update=extend_schema(
        summary="Update a certain cafe",
        description="Admin can update a cafe.",
    ),
    partial_update=extend_schema(
        summary="Partial update a certain cafe",
        description="Admin can make partial update a cafe.",
    ),
    destroy=extend_schema(
        summary="Delete a certain cafe",
        description="Admin can delete a cafe.",
    ),
)
class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return CafeListSerializer
        if self.action == "retrieve":
            return CafeDetailSerializer
        return CafeSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        try:
            return [int(str_id) for str_id in qs.split(",")]
        except ValueError:
            raise ValidationError(code=400, detail="Not a valid list of IDs")

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get("name", None)
        address = self.request.query_params.get("address", None)
        type_ids = self.request.query_params.get("type_ids", None)
        cuisine_ids = self.request.query_params.get("cuisine_ids", None)
        ordering = self.request.query_params.get("ordering", None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if address:
            queryset = queryset.filter(address__icontains=address)
        if type_ids:
            type_ids = self._params_to_ints(type_ids)
            queryset = queryset.filter(type__in=type_ids)
        if cuisine_ids:
            cuisines = self._params_to_ints(cuisine_ids)
            queryset = queryset.filter(cuisine__in=cuisines)
        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except FieldError:
                raise ValidationError(code=400, detail="Invalid ordering")

        return queryset.distinct()

    @extend_schema(
        summary="Get list of cafes",
        description="User can get a list of cafes.",
        methods=["GET"],
        parameters=[
            OpenApiParameter(
                name="type_ids",
                description="Filter by cafe type ids (ex. ?type_ids=2,3)",
                required=False,
                type={"type": "array", "items": {"type": "integer"}},
            ),
            OpenApiParameter(
                name="cuisine_ids",
                description="Filter by cafe cuisines ids (ex. ?cuisine_ids=1,3,6)",
                required=False,
                type={"type": "array", "items": {"type": "integer"}},
            ),
            OpenApiParameter(
                name="name", description="Filter by name", required=False, type=str
            ),
            OpenApiParameter(
                name="address",
                description="Filter by address",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="ordering", description="Ordering cafes", required=False, type=str
            ),
        ],
        examples=[
            OpenApiExample(
                "Example 1",
                value={
                    "types": "1,2,7",
                    "cuisines": "1,6,8",
                },
            ),
            OpenApiExample(
                "Example 2",
                value={
                    "name": "Fenix",
                    "address": "Джона Маккейна",
                },
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve a cafe lunch",
        description="User can get a detail info about cafe lunch.",
    ),
    create=extend_schema(
        summary="Create a cafe lunch",
        description="Admin can create a cafe lunch.",
    ),
    update=extend_schema(
        summary="Update a certain cafe lunch",
        description="Admin can update a cafe lunch.",
    ),
    partial_update=extend_schema(
        summary="Partial update a certain cafe lunch",
        description="Admin can make partial update a cafe lunch.",
    ),
    destroy=extend_schema(
        summary="Delete a certain cafe lunch",
        description="Admin can delete a cafe lunch.",
    ),
)
class CafeLunchMenuViewSet(viewsets.ModelViewSet):
    queryset = CafeLunchMenu.objects.all()
    serializer_class = LunchDishSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CafeLunchMenuDetailSerializer
        return CafeLunchMenuListSerializer

    def get_queryset(self):
        today = datetime.today().strftime("%a").upper()
        queryset = self.queryset.filter(weekday=today)
        cafe_name = self.request.query_params.get("cafe", None)

        if cafe_name:
            queryset = queryset.filter(cafe__name__icontains=cafe_name)

        return queryset

    @extend_schema(
        summary="Get list of cafe lunches",
        description="User can get a list of cafe lunches.",
        methods=["GET"],
        parameters=[
            OpenApiParameter(
                name="name", description="Filter by name", required=False, type=str
            ),
        ],
        examples=[
            OpenApiExample(
                "Example 1",
                value={
                    "name": "Fenix",
                },
            )
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
