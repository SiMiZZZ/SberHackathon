# Generated by Django 4.2 on 2023-04-15 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Experience",
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
                ("date_from", models.DateField()),
                ("date_to", models.DateField()),
                ("descr", models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                ("email", models.CharField(max_length=50)),
                ("password", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=20, null=True)),
                ("surname", models.CharField(max_length=20, null=True)),
                ("patronymic", models.CharField(max_length=20, null=True)),
                ("descr", models.TextField(max_length=1000, null=True)),
                ("is_search", models.BooleanField(max_length=1000, null=True)),
            ],
        ),
    ]
