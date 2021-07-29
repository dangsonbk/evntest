from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Quiz, Grade, Progress, Question, Profile, ProfileUpload, Department, Branch
from multichoice.models import MCQuestion, Answer, Upload
from true_false.models import TF_Question
from essay.models import Essay_Question
class AnswerInline(admin.TabularInline):
    model = Answer

class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label="Danh sách câu hỏi",
        widget=FilteredSelectMultiple(
            verbose_name="Danh sách câu hỏi",
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial =\
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz

class ProfileAdmin(admin.ModelAdmin):
    pass
class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ('title', 'grade', )
    list_filter = ('grade',)
    search_fields = ('description', 'grade', )

class GradeAdmin(admin.ModelAdmin):
    search_fields = ('grade', )

class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'grade', )
    list_filter = ('grade',)
    fields = ('content', 'grade', 'department', 'branch', 'figure', 'quiz', 'explanation', 'answer_order')
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)
    inlines = [AnswerInline]

class ProgressAdmin(admin.ModelAdmin):
    search_fields = ('user', 'score', )

class TFQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'grade', )
    list_filter = ('grade',)
    fields = ('content', 'grade', 'department', 'branch', 'figure', 'quiz', 'explanation', 'correct',)
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

class EssayQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'grade', )
    list_filter = ('grade',)
    fields = ('content', 'grade', 'department', 'branch', 'quiz', 'explanation', )
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Upload)
admin.site.register(ProfileUpload)
admin.site.register(Department)
admin.site.register(Branch)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(TF_Question, TFQuestionAdmin)
admin.site.register(Essay_Question, EssayQuestionAdmin)
admin.site.register(Profile, ProfileAdmin)
