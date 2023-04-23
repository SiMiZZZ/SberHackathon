from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Skill, Vacancy, Test, Test_user, Applicant_employer_responce




class RegistrationSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=30)
    id  = serializers.ReadOnlyField()
    password = serializers.CharField(max_length=200, write_only=True)
    role = serializers.CharField(max_length=20)


    def create(self, validated_data):
        return User.create_user(validated_data["email"], validated_data["password"], validated_data["role"])


class UserSerializer(serializers.ModelSerializer):
    """ Выполняет обновление модели User """

    class Meta:
        model = User
        fields = ["id", "email", "name", "surname", "patronymic", "descr", "is_search", "profession", "city", "birth_day", "img"]

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class VacancySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    img = serializers.CharField()

    class Meta:
        model = Vacancy
        fields = ["id", "name", "salary", "descr", "img"]

    def create(self, validated_data):
        user = User.objects.filter(id=validated_data.pop("id")).first()
        vacancy = Vacancy(**validated_data)
        vacancy.user = user
        vacancy.save()
        return vacancy


class VacanciesSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=30)
    salary = serializers.IntegerField()
    descr = serializers.CharField(max_length=200)
    img = serializers.CharField()

    class Meta:
        model = Vacancy
        fields = ["id", "name", "salary", "descr", "img"]

    def data(self):
        return super.data

class SkillsSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200)

    class Meta:
        model = Skill
        fields = ["name"]

    def data(self):
        return super.data

class TestSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=60)
    descr = serializers.CharField()
    img = serializers.CharField()

    class Meta:
        model = Test
        field = ["id", "name", "descr", "img"]

    # def data(self):
    #     return super.data

class TestUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test_user
        fields = ["test", "user", "result", "is_passed"]

    def create(self, validated_data):
        new_user_test = Test_user(test=validated_data["test"], user=validated_data["user"], result=validated_data["result"] )
        if int(new_user_test.result) >= 60:
            new_user_test.is_passed = True
        new_user_test.save()
        print(new_user_test)
        return new_user_test

class ApplicantEmployerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant_employer_responce
        fields = ["applicant", "vacancy"]

    def create(self, validated_data):
        new_responce = Applicant_employer_responce(applicant=validated_data["applicant"], vacancy=validated_data["vacancy"])
        new_responce.save()
        return new_responce
