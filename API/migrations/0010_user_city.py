# Generated by Django 4.2 on 2023-04-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0009_user_profession"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="city",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
