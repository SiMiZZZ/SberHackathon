# Generated by Django 4.2 on 2023-04-15 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("API", "0004_rename_descr_experience_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name="Role",
        ),
    ]
