from django.urls import path, include
from rest_framework.routers import DefaultRouter

from voting.views import (
    VoteViewSet,
    ResultOfVotingView,
)
router = DefaultRouter()

router.register('results', ResultOfVotingView)
router.register('votes', VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    ]

app_name = "voting"

