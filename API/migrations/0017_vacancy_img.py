# Generated by Django 4.2 on 2023-04-16 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0016_alter_test_descr"),
    ]

    operations = [
        migrations.AddField(
            model_name="vacancy",
            name="img",
            field=models.TextField(null=True),
        ),
    ]