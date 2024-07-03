from django.contrib import admin
from voting.models import Vote, ResultOfVoting
models = [Vote, ResultOfVoting]
for model in models:
    admin.site.register(model)
