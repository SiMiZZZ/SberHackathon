# Generated by Django 4.2 on 2023-04-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0006_user_img"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="birth_day",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="img",
            field=models.ImageField(null=True, upload_to=""),
        ),
    ]