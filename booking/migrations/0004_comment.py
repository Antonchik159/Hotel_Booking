# Generated by Django 5.1.3 on 2024-12-27 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0003_alter_booking_approved"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment",
                    models.TextField(max_length=300, verbose_name="Ваш коментар"),
                ),
                ("comment_date", models.DateTimeField(auto_now_add=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="booking.client"
                    ),
                ),
                (
                    "hostel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="booking.hostel"
                    ),
                ),
            ],
        ),
    ]