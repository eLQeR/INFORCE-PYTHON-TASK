# Generated by Django 5.0.6 on 2024-07-02 17:24

import cafe.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('address', models.CharField(max_length=155)),
                ('cafe_url', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(max_length=55, unique=True)),
                ('main_photo', models.ImageField(default='uploads/Cafe/default.jpg', upload_to=cafe.models.review_image_path)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, unique=True)),
                ('slug', models.SlugField(max_length=155, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstablishmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155, unique=True)),
                ('slug', models.SlugField(max_length=155, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CafeLunchMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=3)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_lunches', to='cafe.cafe')),
            ],
        ),
        migrations.AddField(
            model_name='cafe',
            name='cuisine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafes', to='cafe.cuisine'),
        ),
        migrations.AddField(
            model_name='cafe',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafes', to='cafe.establishmenttype'),
        ),
        migrations.CreateModel(
            name='LunchDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('cost', models.PositiveIntegerField()),
                ('image', models.ImageField(default='uploads/LunchDish/default.jpg', upload_to=cafe.models.review_image_path)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='cafe.cafelunchmenu')),
            ],
        ),
    ]
