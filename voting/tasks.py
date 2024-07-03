from __future__ import absolute_import
import random
import datetime

from celery import shared_task
from django.db.models import Count

from voting.models import Vote, ResultOfVoting
from cafe.models import Cafe


@shared_task
def select_the_winner_cafe():
    today = datetime.date.today()

    # Select all today's votes and group them by cafe

    votes_to_cafes = (
        Vote.objects.filter(created_at=today)
        .values("cafe")
        .annotate(total_votes=Count("id"))
        .order_by("-total_votes")
    )
    if votes_to_cafes:
        most_voted_cafe = votes_to_cafes.first()
        ResultOfVoting.objects.create(
            result_cafe_id=most_voted_cafe["cafe"],
            quantity_of_votes=most_voted_cafe["total_votes"],
        )
    else:
        random_cafe = random.choice(Cafe.objects.all())
        ResultOfVoting.objects.create(result_cafe=random_cafe, quantity_of_votes=0)
