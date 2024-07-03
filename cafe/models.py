import uuid
import pathlib
from typing import Union

from django.db import models
from django.utils.text import slugify


class Cuisine(models.Model):
    name = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name


class EstablishmentType(models.Model):
    name = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(max_length=155, unique=True)

    def __str__(self):
        return self.name


def review_image_path(instance: Union["Cafe", "LunchDish"], filename: str) -> pathlib.Path:
    filename = f"{instance.name}-{slugify(filename)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    return pathlib.Path(f"uploads/{instance.__class__.__name__}/") / pathlib.Path(filename)


class Cafe(models.Model):
    name = models.CharField(max_length=155)
    address = models.CharField(max_length=155)
    slug = models.SlugField(max_length=255, unique=True)
    cafe_url = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=55, unique=True)
    type = models.ForeignKey(to=EstablishmentType, on_delete=models.CASCADE, related_name="cafes")
    cuisine = models.ForeignKey(to=Cuisine, on_delete=models.CASCADE, related_name="cafes")
    main_photo = models.ImageField(
        upload_to=review_image_path,
        default="uploads/Cafe/default.jpg"
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class CafeLunchMenu(models.Model):
    class Weekdays(models.TextChoices):
        MON = ('MON', 'Monday')
        TUE = ('TUE', 'Tuesday')
        WED = ('WED', 'Wednesday')
        THU = ('THU', 'Thursday')
        FRI = ('FRI', 'Friday')
        SAT = ('SAT', 'Saturday')
        SUN = ('SUN', 'Sunday')

    cafe = models.ForeignKey(to=Cafe, on_delete=models.CASCADE, related_name='menu_lunches')
    weekday = models.CharField(max_length=3, choices=Weekdays.choices)

    def __str__(self):
        return f"{self.cafe.name}, {self.weekday}"


class LunchDish(models.Model):
    name = models.CharField(max_length=155)
    cost = models.PositiveIntegerField()
    image = models.ImageField(upload_to=review_image_path, default="uploads/LunchDish/default.jpg")
    menu = models.ForeignKey(
        to=CafeLunchMenu,
        on_delete=models.CASCADE,
        related_name="dishes"
    )

