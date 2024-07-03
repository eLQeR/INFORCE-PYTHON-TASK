from django.db import transaction
from rest_framework import serializers
from voting.models import Vote, ResultOfVoting
from cafe.serializers import CafeListSerializer, CafeDetailSerializer


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = (
            "id",
            "cafe",
            "voter",
            "created_at",
        )


class VoteListSerializer(serializers.ModelSerializer):
    cafe = CafeListSerializer(many=False, read_only=True)

    class Meta:
        model = Vote
        fields = (
            "id",
            "cafe",
            "created_at",
        )


class ResultOfVotingListSerializer(serializers.ModelSerializer):
    result_cafe = CafeListSerializer(many=False, read_only=True)

    class Meta:
        model = ResultOfVoting
        fields = (
            "id",
            "voting_date",
            "result_cafe",
            "quantity_of_votes",
        )


class ResultOfVotingDetailSerializer(serializers.ModelSerializer):
    result_cafe = CafeDetailSerializer(many=False, read_only=True)

    class Meta:
        model = ResultOfVoting
        fields = (
            "id",
            "voting_date",
            "result_cafe",
            "quantity_of_votes",
        )
