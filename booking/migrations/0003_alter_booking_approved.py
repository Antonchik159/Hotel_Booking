# Generated by Django 5.1.3 on 2024-12-18 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_client_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="approved",
            field=models.BooleanField(null=True),
        ),
    ]
