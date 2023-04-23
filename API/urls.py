from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns =[
    path("auth/registration/", RegistrationAPIView.as_view()),
    path("auth/login/", AutorisationAPIView.as_view()),
    path("user/", UserUpdateAPIView.as_view()),
    path("skills/", SkillsAPIView.as_view()),
    path("vacancy/", VacancyAPIView.as_view()),
    path("vacancies/", VacanciesAPIView.as_view()),
    path("vacancy/<int:vacancy_id>/", VacancyAPIView.as_view()),
    path("user/<int:user_id>", UserAPIView.as_view()),
    path("user/<int:user_id>/vacancies", VacanciesByUserAPIView.as_view()),
    path("tests/", TestsAPIView.as_view()),
    path("test/<int:test_id>", TestAPIView.as_view()),
    path("users/applicants", ApplicantsAPIView.as_view()),
    path("test/user", TestUserApiView.as_view()),
    path("test/user/<int:user_id>", TestUserApiView.as_view()),
    path("applicant/employer", ApplicantEmployerApiView.as_view()),
    path("employer/applicant", ApplicantsAPIView.as_view())
]