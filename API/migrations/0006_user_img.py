# Generated by Django 4.2 on 2023-04-15 19:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0005_alter_user_role_delete_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="img",
            field=models.ImageField(default=django.utils.timezone.now, upload_to=""),
            preserve_default=False,
        ),
    ]
