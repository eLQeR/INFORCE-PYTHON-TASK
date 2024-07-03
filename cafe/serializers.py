from django.db import transaction
from rest_framework import serializers
from cafe.models import Cafe, EstablishmentType, Cuisine, CafeLunchMenu, LunchDish


class EstablishmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentType
        fields = ("id", "name", "slug")


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ("id", "name", "slug")


class LunchDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = LunchDish
        fields = ("id", "name", "cost", "image", "menu")


class LunchDishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LunchDish
        fields = ("id", "name", "cost")


class LunchDishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LunchDish
        fields = ("id", "name", "cost", "image")


class CafeLunchMenuListSerializer(serializers.ModelSerializer):
    dishes = LunchDishListSerializer(many=True, read_only=True)

    class Meta:
        model = CafeLunchMenu
        fields = ("id", "cafe", "weekday", "dishes")


class CafeLunchMenuDetailSerializer(CafeLunchMenuListSerializer):
    dishes = LunchDishDetailSerializer(many=True, read_only=True)


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = (
            "id",
            "name",
            "address",
            "type",
            "cuisine",
            "main_photo",
        )


class CafeListSerializer(CafeSerializer):
    type = serializers.CharField(source="type.name", read_only=True)

    class Meta:
        model = Cafe
        fields = (
            "id",
            "name",
            "address",
            "type",
            "slug",
            "main_photo",
        )


class CafeDetailSerializer(CafeListSerializer):
    menu_lunches = CafeLunchMenuDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Cafe
        fields = (
            "id",
            "name",
            "address",
            "type",
            "slug",
            "main_photo",
            "description",
            "menu_lunches",
        )
