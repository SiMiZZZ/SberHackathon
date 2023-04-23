from django.db import models



class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=200)

    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    patronymic = models.CharField(max_length=20, null=True)

    descr = models.TextField(max_length=1000, null=True)
    is_search = models.BooleanField(max_length=1000, null=True)
    role = models.CharField(max_length=20, null=True)
    birth_day = models.DateField(null=True)
    img = models.TextField(null=True)
    profession = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)


    @staticmethod
    def create_user(email, password, role):
        new_user = User(email=email, password=password, role=role)
        new_user.save()
        return new_user



class Skill(models.Model):
    name = models.CharField(max_length=30, default="Маркетинг")
    trajectory = models.CharField(max_length=30, default="Аналитика")

    def __str__(self):
        return self.name


class User_skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True)


class Vacancy(models.Model):
    name = models.CharField(max_length=30, null=True)
    salary = models.IntegerField(null=True)
    descr = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    img = models.TextField(null=True)


class Test(models.Model):
    name = models.CharField(max_length=200, null=True)
    descr = models.TextField(null=True)
    img = models.TextField(null=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    question = models.TextField(max_length=300, null=True)
    correct_answer = models.TextField(null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question

class Answer(models.Model):
    body = models.CharField(max_length=100, null=True)
    is_true = models.BooleanField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.body


class Test_user(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    result = models.IntegerField(null=True)
    is_passed = models.BooleanField(default=False)


class Applicant_employer_responce(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Applicant_link", null=True)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True)





