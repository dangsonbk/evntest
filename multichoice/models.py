from __future__ import unicode_literals
from unicodedata import category
from django.utils.translation import ugettext_lazy as _
from django.db import models
from quiz.models import Question, Category, SubCategory, Quiz
from django import forms
from openpyxl import load_workbook
import urllib.parse
import re


ANSWER_ORDER_OPTIONS = (
    ('content', _('Nội dung')),
    ('random', _('Ngẫu nhiên')),
    ('none', _('Không chọn'))
)

class MCQuestion(Question):

    answer_order = models.CharField(max_length=30, null=True, blank=True, choices=ANSWER_ORDER_OPTIONS, help_text=_("The order in which multichoice answer options are displayed to the user"),verbose_name=_("Answer Order"))

    def check_if_correct(self, guess):
        answer = Answer.objects.get(id=guess)
        return answer.correct

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in self.order_answers(Answer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = _("Câu hỏi nhiều lựa chọn")
        verbose_name_plural = _("Câu hỏi nhiều lựa chọn")

class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name=_("Câu hỏi"), on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False, help_text="Câu trả lời", verbose_name=_("Content"))
    correct = models.BooleanField(blank=False, default=False, help_text="Câu trả lời đúng", verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Câu trả lời")
        verbose_name_plural = _("Câu trả lời")
class Upload(models.Model):
    quiz_file = models.FileField(upload_to='sample_quiz')
    category = models.ForeignKey(Category, verbose_name="Phân loại", null=True, blank=True, on_delete=models.CASCADE)
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
            sub_cat = ""
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
                    if not sub_cat:
                        sub_cat = row[0].value.strip()
                    else:
                        quiz_title = row[0].value.strip()
            if sub_cat and quiz_title:
                # Create sub cat
                sub1 = SubCategory.objects.create(sub_category=sub_cat, category=self.category)
                # Create quiz
                quiz = Quiz.objects.create( title=quiz_title, description=quiz_title, url=urllib.parse.quote(quiz_title).lower(), pass_mark=50,
                                            success_text="Bạn đã hoàn thành bài thi", fail_text="Bạn đã không hoàn thành bài thi")
                # Append question
                for question in question_list["questions"]:
                    ques = MCQuestion.objects.create(category=self.category, sub_category=sub1, content=question["question"])
                    ques.quiz.add(quiz)
                    for choice in question["multichoices"]:
                        answer = Answer.objects.create( question=ques,
                                                        content=question["multichoices"][choice], correct=(question["answer"] == choice))

            print(question_list)

    def __str__(self) -> str:
        return self.quiz_file.name

    class Meta:
        verbose_name = "Tải lên danh sách câu hỏi"
        verbose_name_plural = "Tải lên danh sách câu hỏi"