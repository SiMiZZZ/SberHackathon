from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

import hashlib
from .models import User, User_skill, Skill, Test, Task, Answer

class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        user_data = request.data
        emails = list(map(lambda x: x["email"], User.objects.values("email")))

        if len(list(emails)) != 0:
            if user_data["email"] in emails:
                return Response({"error": "Пользователь с таким email уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        user_data["password"] = hash_text(user_data["password"])

        user = User(email=user_data["email"], password=user_data["password"], role=user_data["role"])


        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer.data["id"] = user.id
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        user_id = serializer_data["id"]

        user = User.objects.filter(id=user_id).first()

        serializer = self.serializer_class(user, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)
        if "skills" in serializer_data:
            self.update_skills(serializer_data, user_id)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


    def update_skills(self, data, user_id):
        User_skill.objects.filter(id=user_id).delete()
        skills_array = data.get("skills")
        user = User.objects.filter(id=user_id).first()
        for skill in skills_array:
            new_skill = User_skill(skill=Skill.objects.filter(name=skill).first(), user=user)
            new_skill.save()


class AutorisationAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer_data = request.data

        user_email = serializer_data.get("email")
        emails = list(map(lambda x: x["email"], User.objects.values("email")))

        if user_email not in emails:
            return Response({"error": "Пользователя с таким email не существует"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=user_email).first()
        hash_password = hash_text(serializer_data["password"])

        print(user.password, hash_password)
        if user.password == hash_password:
            serializer_data["role"] = user.role
            serializer_data["id"] = user.id
            return Response(serializer_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Ввёден неверный логин или пароль"}, status=status.HTTP_400_BAD_REQUEST)


def hash_text(text):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()


class VacancyAPIView(APIView):
    serializer_class = VacancySerializer

    def post(self, request):
        serializer_data = request.data
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, vacancy_id=3):
        serializer_data = Vacancy.objects.filter(id=vacancy_id).first()
        serializer = self.serializer_class(serializer_data)

        employer = serializer_data.user
        response_data = dict(serializer.data)
        response_data["employer_id"] = employer.id
        response_data["employer_name"] = employer.name

        return Response(response_data, status=status.HTTP_200_OK)

class VacanciesAPIView(APIView):
    serializer_class = VacanciesSerializer

    def get(self, request, vacancy_id=None):
        serializer_data = Vacancy.objects.all()
        serializer = self.serializer_class(data=serializer_data, many=True)
        serializer.is_valid()


        return Response(serializer.data, status=status.HTTP_200_OK)


class SkillsAPIView(APIView):
    serializer_class = SkillsSerializer

    def get(self, request):
        serializer_data = Skill.objects.all()
        serializer = self.serializer_class(data=serializer_data, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VacancyAPIView(APIView):
    serializer_class = VacancySerializer

    def post(self, request):
        serializer_data = request.data
        serializer = self.serializer_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, vacancy_id=3):
        serializer_data = Vacancy.objects.filter(id=vacancy_id).first()
        serializer = self.serializer_class(serializer_data)

        employer = serializer_data.user
        response_data = dict(serializer.data)
        response_data["employer_id"] = employer.id
        response_data["employer_name"] = employer.name

        return Response(response_data, status=status.HTTP_200_OK)


class UserAPIView(APIView):
    serializer_class = UserSerializer

    def get(self, request, user_id=None):
        serializer_data = User.objects.filter(id=user_id).first()
        serializer = self.serializer_class(serializer_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

class VacanciesByUserAPIView(APIView):
    serializer_class = VacancySerializer

    def get(self, request, user_id=None):
        user = User.objects.filter(id=user_id).first()
        serializer_data = Vacancy.objects.filter(user=user).all()

        serializer = self.serializer_class(serializer_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TestsAPIView(APIView):
    serializer_class = TestSerializer

    def get(self, request):
        tests = Test.objects.all()
        serializer = self.serializer_class(tests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAPIView(APIView):
    serializer_class = TestSerializer

    def get(self, request, test_id=None):
        test = Test.objects.filter(id=test_id).first()
        serializer = self.serializer_class(test)

        result_data = dict(serializer.data)

        tasks = Task.objects.filter(test=test).all()
        result_data["tasks"] = []
        for i, task in enumerate(tasks):
            task_dct = {"question": task.question, "correct_answer": task.correct_answer, "answers": []}
            answers = Answer.objects.filter(task=task).all()
            for answer in answers:
                task_dct["answers"].append(answer.body)
            result_data["tasks"].append(task_dct)

        return Response(result_data, status=status.HTTP_200_OK)

class ApplicantsAPIView(APIView):
    serializers_class = UserSerializer

    def get(self, request):
        serializer_data = User.objects.filter(role="applicant").all()
        serializer = self.serializers_class(serializer_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TestUserApiView(APIView):
    serializers_class = TestUserSerializer

    def post(self, request):
        test_id = request.data.get("test")
        user_id = request.data.get("user")

        test = Test.objects.filter(id=test_id).first()
        user = User.objects.filter(id=user_id).first()

        result = request.data.get("result")

        serializer_data = {"test": test.id, "user": user.id, "result": result}

        serializer = self.serializers_class(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, user_id=None):
        serializer_data = User.objects.filter(id=user_id).first()
        serializer = self.serializers_class(serializer_data)

        return_dict = dict(serializer.data)
        tests = Test_user.objects.filter(user=user_id).all()
        return_dict["tests"] = []
        for test in tests:
            result_test = {"name": test.test.name, "is_passed": test.is_passed}
            return_dict["tests"].append(result_test)

        return Response(return_dict, status=status.HTTP_200_OK)

class ApplicantEmployerApiView(APIView):
    serializer_class = ApplicantEmployerSerializer

    def post(self, request):
        data = request.data
        applicant_id = data.get("applicant")
        vacancy_id = data.get("vacancy")
        serialized_data = {"applicant": applicant_id, "vacancy": vacancy_id}
        serializer = self.serializer_class(data=serialized_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)


        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        vacancy_id = request.GET.get("vacancy_id")
        applicant_id = request.GET.get("applicant_id")
        responces = Applicant_employer_responce.objects.filter(vacancy=vacancy_id).filter(applicant=applicant_id).all()
        serializers = self.serializer_class(responces, many=True)

        return Response(serializers, status=status.HTTP_200_OK)
