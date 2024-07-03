from django.contrib.auth import get_user_model
from django.db import models

from cafe.models import Cafe


class ResultOfVoting(models.Model):
    voting_date = models.DateField(auto_now_add=True)
    result_cafe = models.ForeignKey(to=Cafe, on_delete=models.CASCADE, related_name='results_voting')
    quantity_of_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ('-voting_date',)


class Vote(models.Model):
    cafe = models.ForeignKey(to=Cafe, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateField(auto_now_add=True)
    voter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='votes')

    class Meta:
        unique_together = (('created_at', 'voter'),)
        ordering = ('-created_at',)
