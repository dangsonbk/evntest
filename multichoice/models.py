from __future__ import unicode_literals
from unicodedata import category
from django.db import models
from quiz.models import Question, Quiz, Department, Branch, Grade
from django import forms
from openpyxl import load_workbook
import urllib.parse
import re


ANSWER_ORDER_OPTIONS = (
    ('content', 'Nội dung'),
    ('random', 'Ngẫu nhiên'),
    ('none', 'Không chọn')
)

class MCQuestion(Question):

    answer_order = models.CharField(max_length=30, null=True, blank=True, choices=ANSWER_ORDER_OPTIONS, help_text="Cách thức hiển thị câu trả lời trên bài thi", verbose_name="Thứ tự câu trả lời")

    def check_if_correct(self, guess):
        answer = Answer.objects.get(id=guess)
        return answer.correct

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by('?')
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in self.order_answers(Answer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = "Câu hỏi nhiều lựa chọn"
        verbose_name_plural = "Câu hỏi nhiều lựa chọn"

class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name="Câu hỏi", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False, help_text="Câu trả lời", verbose_name="Nội dung")
    correct = models.BooleanField(blank=False, default=False, help_text="Câu trả lời đúng", verbose_name="Tick vào câu trả lời đúng")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Câu trả lời"
        verbose_name_plural = "Câu trả lời"

class Upload(models.Model):
    quiz_file = models.FileField(upload_to='quiz')
    grade = models.ForeignKey(Grade, verbose_name="Bậc thợ", null=True, blank=True, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, verbose_name="Phòng ban", null=True, blank=True, on_delete=models.DO_NOTHING)
    branch = models.ForeignKey(Branch, verbose_name="Chi nhánh", null=True, blank=True, on_delete=models.DO_NOTHING)
    imported = models.BooleanField(default=False, verbose_name="Đã nạp câu hỏi")
    def save(self, *args, **kwargs):
        self.imported = True
        super().save(*args, **kwargs)
        self.import_worksheet()

    def import_worksheet(self):
        wbs = load_workbook(self.quiz_file.path)
        for wb in wbs:
            # Find start of quiz table
            start_of_quiz_table = False
            question_list = {"name": wb.title, "questions": []}
            quiz_title = ""
            for row in wb:
                if start_of_quiz_table and row[0].value:
                    regx = re.search("(Câu \d+).(.+)", row[1].value)
                    if regx:
                        multichoices = {}
                        question = regx.group(2).strip()
                        if question[-1] == ":" or question[-1] == "?":
                            question = question[:-1]
                        for q in [row[2].value, row[3].value, row[4].value, row[5].value]:
                            if q is None:
                                continue
                            regx = re.search("([abcd])\.(.+)", q)
                            if regx:
                                multichoices[regx.group(1).strip().upper()] = regx.group(2).strip()
                        question_list["questions"].append({"question": question, "multichoices": multichoices, "answer": row[6].value})
                    else:
                        print("Question format does not match: ", row[1].value)
                if row[0].value == "STT":
                    start_of_quiz_table = True
                if not start_of_quiz_table and row[0].value :
                    quiz_title = row[0].value.strip()
            if quiz_title:
                # Create quiz
                quiz = Quiz.objects.create( title=quiz_title, description=quiz_title, url=urllib.parse.quote(quiz_title).lower(), pass_mark=50,
                                            success_text="Bạn đã hoàn thành bài thi", fail_text="Bạn đã không hoàn thành bài thi")
                # Append question
                for question in question_list["questions"]:
                    ques = None
                    ques, created = MCQuestion.objects.get_or_create(grade=self.grade, department=self.department, branch=self.branch, content=question["question"])
                    ques.quiz.add(quiz)
                    if not created:
                        for choice in question["multichoices"]:
                            answer = Answer.objects.create( question=ques, content=question["multichoices"][choice], correct=(question["answer"] == choice))
            print(question_list)

    def __str__(self) -> str:
        return self.quiz_file.name

    class Meta:
        verbose_name = "Tải lên danh sách câu hỏi"
        verbose_name_plural = "Tải lên danh sách câu hỏi"