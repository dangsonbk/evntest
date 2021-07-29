from __future__ import unicode_literals
import re
import json

from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.utils.timezone import now
from django.conf import settings

from model_utils.managers import InheritanceManager
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from openpyxl import load_workbook

GENDER_CHOICES = [
    ("0", "Nam"),
    ("1", "Nữ"),
]

class CategoryManager(models.Manager):

    def new_category(self, category):
        new_category = self.get_or_create(category=re.sub('\s+', '-', category).lower())
        new_category.save()
        return new_category

class Category(models.Model):
    category = models.CharField(verbose_name="Phân loại", max_length=250, blank=True, unique=True, null=True)
    objects = CategoryManager()
    class Meta:
        verbose_name = "Phân loại"
        verbose_name_plural = "Phân loại"

    def __str__(self):
        return self.category

class SubCategory(models.Model):

    sub_category = models.CharField(verbose_name="Phân loại nhỏ", max_length=250, blank=True, null=True)
    category = models.ForeignKey(Category, null=True, blank=True,verbose_name="Phân loại chính", on_delete=models.CASCADE)
    objects = CategoryManager()

    class Meta:
        verbose_name = "Phân loại nhỏ"
        verbose_name_plural = "Phân loại nhỏ"

    def __str__(self):
        return self.sub_category + " (" + self.category.category + ")"

class Department(models.Model):
    department = models.CharField(verbose_name="Phòng ban", max_length=512, null=True, blank=True)
    def __str__(self) -> str:
        return self.department
    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Phòng ban"

class Branch(models.Model):
    branch = models.CharField(verbose_name="Chi nhánh", max_length=512, null=True, blank=True)
    def __str__(self) -> str:
        return self.branch
    class Meta:
        verbose_name = "Chi nhánh"
        verbose_name_plural = "Chi nhánh"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name="Họ tên", max_length=100, null=True, blank=True)
    gender = models.CharField(verbose_name="Giới tính", max_length=1, choices=GENDER_CHOICES, default="0")
    department = models.ForeignKey(Department, null=True, verbose_name="Phòng ban", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Chức danh", max_length=512, null=True, blank=True)
    dob = models.CharField(verbose_name="Ngày sinh", max_length=10, null=True, blank=True)
    id_card = models.CharField(max_length=12, null=True, blank=True)
    branch = models.ForeignKey(Branch, null=True, verbose_name="Chi nhánh", on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = "Thí sinh"
        verbose_name_plural = "Thí sinh"
    
    def __str__(self) -> str:
        return "".join([str(self.user), "-", str(self.full_name)])

class ProfileUpload(models.Model):
    profile_file = models.FileField(upload_to='profile_list')
    branch = models.ForeignKey(Branch, null=True, verbose_name="Chi nhánh", on_delete=models.DO_NOTHING)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.import_worksheet()

    def import_worksheet(self):
        start_of_quiz_table = False
        user_list = []
        wbs = load_workbook(self.profile_file.path)

        for row in wbs.worksheets[0]:
            if start_of_quiz_table and row[1].value and row[2].value and row[3].value and row[4].value:
                _user = User.objects.get_or_create(username=str(row[0].value))
                _department = Department.objects.get_or_create(department=row[4].value)
                _profile = Profile.objects.update_or_create(
                    user=_user[0],
                    defaults={
                        'full_name': row[1].value,
                        'gender': row[3].value,
                        'department': _department[0],
                        'title': "nhân viên",
                        'dob': row[2].value,
                        'id_card':str(row[0].value),
                        'branch': self.branch
                    }
                )
            if row[0].value == "mahocvien":
                start_of_quiz_table = True
                print("Start of quiz table found, starting to import")

    def __str__(self) -> str:
        return self.profile_file.name

    class Meta:
        verbose_name = "Tải lên danh sách thí sinh"
        verbose_name_plural = "Tải lên danh sách thí sinh"

class Quiz(models.Model):

    title = models.CharField(verbose_name="Tên bài thi", max_length=60, blank=False)
    description = models.TextField(verbose_name="Chi tiết", blank=True, help_text="Thông tin bài thi")
    url = models.SlugField(max_length=60, blank=False, help_text="Đường dẫn tới bài thi", verbose_name="Đường dẫn")
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name="Phân loại", on_delete=models.CASCADE)
    random_order = models.BooleanField(blank=False, default=False, verbose_name="Câu hỏi ngẫu nhiên", help_text="Sắp xếp câu hỏi ngẫu nhiên")
    max_questions = models.PositiveIntegerField(blank=True, null=True, verbose_name="Số câu hỏi", help_text="Số lượng câu hỏi tối đa.")
    answers_at_end = models.BooleanField(blank=False, default=False, help_text="Hiển thị kết quả sau khi nộp bài", verbose_name="Xem kết quả")
    exam_paper = models.BooleanField(blank=False, default=False,help_text="Hiển thị toàn bộ câu hỏi một lần", verbose_name="Hiển thị toàn bộ câu hỏi")
    single_attempt = models.BooleanField(blank=False, default=False, help_text="Chỉ cho phép thi một lần hoặc nhiều lần", verbose_name="Thi một lần")
    pass_mark = models.SmallIntegerField(blank=True, default=0, verbose_name="Điểm tối thiểu", help_text="Điểm tối thiểu để đạt", validators=[MaxValueValidator(100)])
    success_text = models.TextField(blank=True, help_text="Thông báo thi đạt", verbose_name="Thông báo thi đạt")
    fail_text = models.TextField(verbose_name="Thông báo thi trượt", blank=True, help_text="Thông báo thi trượt")
    draft = models.BooleanField(blank=True, default=False, verbose_name="Draft", help_text="If yes, the quiz is not displayed in the quiz list and can only be taken by users who can edit quizzes.")
    start = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian mở đề")
    end = models.DateTimeField(null=True, blank=True, verbose_name="Hạn cuối làm bài")
    duration = models.IntegerField(default=30, verbose_name="Thời gian làm bài")
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.url = re.sub('\s+', '-', self.url).lower()
        self.url = ''.join(letter for letter in self.url if letter.isalnum() or letter == '-')

        if self.single_attempt is True:
            self.exam_paper = True

        if self.pass_mark > 100:
            raise ValidationError('%s trên 100' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = "Đề thi"
        verbose_name_plural = "Đề thi"

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()

    def anon_score_id(self):
        return str(self.id) + "_score"

    def anon_q_list(self):
        return str(self.id) + "_q_list"

    def anon_q_data(self):
        return str(self.id) + "_data"


class ProgressManager(models.Manager):

    def new_progress(self, user):
        new_progress = self.create(user=user, score="")
        new_progress.save()
        return new_progress


class Progress(models.Model):
    """
    Progress is used to track an individual signed in users score on different
    quiz's and categories

    Data stored in csv using the format: category, score, possible, category, score, possible, ...
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Thí sinh", on_delete=models.CASCADE)
    score = models.CharField(max_length=1024, verbose_name="Điểm", validators=[validate_comma_separated_integer_list])
    objects = ProgressManager()

    def __str__(self) -> str:
        return "".join((str(self.user), ))

    class Meta:
        verbose_name = "Bài làm của thí sinh"
        verbose_name_plural = "Bài làm của thí sinh"

    @property
    def list_all_cat_scores(self):
        """
        Returns a dict in which the key is the category name and the item is
        a list of three integers.

        The first is the number of questions correct,
        the second is the possible best score,
        the third is the percentage correct.

        The dict will have one key for every category that you have defined
        """
        score_before = self.score
        output = {}

        for cat in Category.objects.all():
            to_find = re.escape(cat.category) + r",(\d+),(\d+),"
            #  group 1 is score, group 2 is highest possible

            match = re.search(to_find, self.score, re.IGNORECASE)

            if match:
                score = int(match.group(1))
                possible = int(match.group(2))

                try:
                    percent = int(round((float(score) / float(possible)) * 100))
                except:
                    percent = 0

                output[cat.category] = [score, possible, percent]

            else:  # if category has not been added yet, add it.
                self.score += cat.category + ",0,0,"
                output[cat.category] = [0, 0]

        if len(self.score) > len(score_before):
            # If a new category has been added, save changes.
            self.save()

        return output

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        """
        Pass in question object, amount to increase score
        and max possible.

        Does not return anything.
        """
        category_test = Category.objects.filter(category=question.category).exists()

        if any([item is False for item in [category_test, score_to_add, possible_to_add, isinstance(score_to_add, int), isinstance(possible_to_add, int)]]):
            return "error", "category does not exist or invalid score"

        to_find = re.escape(str(question.category)) + r",(?P<score>\d+),(?P<possible>\d+),"
        match = re.search(to_find, self.score, re.IGNORECASE)

        if match:
            updated_score = int(match.group('score')) + abs(score_to_add)
            updated_possible = int(match.group('possible')) + abs(possible_to_add)
            new_score = ",".join([str(question.category), str(updated_score), str(updated_possible), ""])
            # swap old score for the new one
            self.score = self.score.replace(match.group(), new_score)
            self.save()

        else:
            #  if not present but existing, add with the points passed in
            self.score += ",".join([str(question.category), str(score_to_add), str(possible_to_add), ""])
            self.save()

    def show_exams(self):
        """
        Finds the previous quizzes marked as 'exam papers'.
        Returns a queryset of complete exams.
        """
        return Sitting.objects.filter(user=self.user, complete=True)


class SittingManager(models.Manager):

    def new_sitting(self, user, quiz):
        if quiz.random_order is True:
            question_set = quiz.question_set.all().select_subclasses().order_by('?')
        else:
            question_set = quiz.question_set.all().select_subclasses()
        question_set = [item.id for item in question_set]
        if len(question_set) == 0:
            raise ImproperlyConfigured('Question set of the quiz is empty. Please configure questions properly')

        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set = question_set[:quiz.max_questions]
        questions = ",".join(map(str, question_set)) + ","
        new_sitting = self.create(user=user, quiz=quiz, question_order=questions, question_list=questions, incorrect_questions="", current_score=0, complete=False, user_answers='{}')
        return new_sitting

    def user_sitting(self, user, quiz):
        if quiz.single_attempt is True and self.filter(user=user, quiz=quiz, complete=True).exists():
            return False
        try:
            sitting = self.get(user=user, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(user, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(user=user, quiz=quiz, complete=False)[0]
        return sitting

class Sitting(models.Model):
    """
    Used to store the progress of logged in users sitting a quiz.
    Replaces the session system used by anon users.
    Question_order is a list of integer pks of all the questions in the
    quiz, in order.
    Question_list is a list of integers which represent id's of
    the unanswered questions in csv format.
    Incorrect_questions is a list in the same format.
    Sitting deleted when quiz finished unless quiz.exam_paper is true.
    User_answers is a json object in which the question PK is stored
    with the answer the user gave.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Thí sinh", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, verbose_name="Quiz", on_delete=models.CASCADE)
    question_order = models.CharField(max_length=1024, verbose_name="Thứ tự câu hỏi", validators=[validate_comma_separated_integer_list])
    question_list = models.CharField(max_length=1024, verbose_name="Danh sách câu hỏi", validators=[validate_comma_separated_integer_list])
    incorrect_questions = models.CharField(max_length=1024, blank=True, verbose_name="Câu hỏi sai", validators=[validate_comma_separated_integer_list])
    current_score = models.IntegerField(verbose_name="Điểm hiện tại")
    complete = models.BooleanField(default=False, blank=False,verbose_name="Hoàn thành")
    user_answers = models.TextField(blank=True, default='{}',verbose_name="Câu trả lời của thí sinh")
    start = models.DateTimeField(auto_now_add=True, verbose_name="Bắt đầu")
    end = models.DateTimeField(null=True, blank=True, verbose_name="Kết thúc")
    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", "Có thể xem toàn bộ bài thi."),)

    def get_first_question(self):
        """
        Returns the next question.
        If no question is found, returns False
        Does NOT remove the question from the front of the list.
        """
        if not self.question_list:
            return False

        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.get_subclass(id=question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, others = self.question_list.split(',', 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(',') if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0            # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        """
        Adds uid of incorrect question to the list.
        The question object must be passed in.
        """
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ','
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        """
        Returns a list of non empty integers, representing the pk of
        questions
        """
        return [int(q) for q in self.incorrect_questions.split(',') if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(self.quiz.question_set.filter(id__in=question_ids).select_subclasses(), key=lambda q: question_ids.index(q.id))

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[str(question.id)]

        return questions

    @property
    def questions_with_user_answers(self):
        return {q: q.user_answer for q in self.get_questions(with_answers=True)}

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        """
        Returns the number of questions answered so far and the total number of questions.
        """
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total


class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """
    quiz = models.ManyToManyField(Quiz, verbose_name="Quiz", blank=True)
    category = models.ForeignKey(Category, verbose_name="Category", blank=True, null=True, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, verbose_name="Sub-Category", blank=True, null=True, on_delete=models.CASCADE)
    figure = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, null=True, verbose_name="Figure")
    content = models.CharField(max_length=1000, blank=False, help_text="Enter the question text that you want displayed", verbose_name='Question')
    explanation = models.TextField(max_length=2000, blank=True, help_text="Explanation to be shown after the question has been answered.", verbose_name='Explanation')
    objects = InheritanceManager()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['category']

    def __str__(self):
        return self.content