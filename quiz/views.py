import random
import time
import datetime
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView, UpdateView
from django.contrib.auth import views, login as auth_login

from .forms import QuestionForm, EssayForm, QuizProfileForm
from .models import Department, Quiz, Grade, Progress, Sitting, Question, Profile
from essay.models import Essay_Question

class CustomLoginView(views.LoginView):
    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return redirect(reverse('quiz_index'))

def QuizWelcomeView(request):
    return render(request=request, template_name="quiz/quiz_welcome.html")

class QuizProfileView(UpdateView):
    model = Profile
    template_name = 'quiz/user_profile.html'
    form_class = QuizProfileForm
    success_url = '/'

    def form_valid(self, form):
        redirect_url = super(QuizProfileView, self).form_valid(form)
        user_obj = form.instance.user
        user_obj.first_name = form.cleaned_data['full_name']
        user_obj.save()
        return redirect_url

class QuizMarkerMixin(object):
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_list.html'

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        queryset = queryset.filter(draft=False)
        profile = Profile.objects.get(user=self.request.user)
        grade = profile.grade
        depart = profile.department
        branch = profile.branch
        if grade:
            queryset = queryset.filter(grade=grade, department=depart, branch=branch)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_header'] = "Danh sách bài thi"
        return context

class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'
    template_name = 'quiz/quiz_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        if not context['quiz']:
            return redirect(reverse('quiz_index'))
        context['main_header'] = "Thông tin bài thi"

        return self.render_to_response(context)

class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset().filter(complete=True)
        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] = context['sitting'].get_questions(with_answers=True)
        return context


class QuizTake(FormView):
    form_class = QuestionForm
    # template_name = 'question.html'
    template_name = 'quiz/question.html'
    result_template_name = 'quiz/result.html'
    single_complete_template_name = 'single_complete.html'
    login_request_template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        self.quizurl = self.kwargs['quiz_name']
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        try:
            self.logged_in_user = self.request.user.is_authenticated()
        except TypeError:
            self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user, self.quiz)
        else:
            return render(request, self.login_request_template_name)

        if "question_number" in kwargs:
            self.question_number = self.kwargs['question_number']
        else:
            self.question_number = None

        if self.sitting is False:
            return render(request, self.single_complete_template_name)
        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.question, self.answer = self.sitting.get_question(self.question_number)
        if self.question.__class__ is Essay_Question:
            form_class = EssayForm
        else:
            form_class = self.form_class
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question, initial={"answers": self.answer})

    def form_valid(self, form):
        guess = form.cleaned_data['answers']
        self.sitting.add_user_answer(self.question, guess)
        self.request.POST = {}
        return redirect("/{}/take/{}".format(self.quizurl, self.sitting.get_next_question_id(self.question_number)))

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['answer'] = self.answer
        context['quiz'] = self.quiz
        context['main_header'] = self.quiz
        context['questions'] = map(int, self.sitting.question_order[:-1].split(","))
        context['answered'] = list(map(int, json.loads(self.sitting.user_answers).keys()))
        context['previous_id'] = self.sitting.get_previous_question_id(self.question_number)

        if not context['quiz']:
            return redirect(reverse('quiz_index'))

        sid = f'tf-{self.quiz.id}'
        current_time = int(time.time())
        if sid not in self.request.session:
            expired = current_time + (self.quiz.duration * 60)
            self.request.session[sid] = expired
        else:
            expired = self.request.session[sid]

        time_left = expired - current_time
        if time_left < 1:
            time_left = 0
        context['time_left_s'] = time_left
        if time_left < 1:
            context['time_left_f'] = 'Hết giờ'
        else:
            context['time_left_f'] = datetime.timedelta(seconds=time_left)
        return context

    def final_result_user(self):
        results = { 'quiz': self.quiz, 'score': self.sitting.get_current_score,'max_score': self.sitting.get_max_score,'percent': self.sitting.get_percent_correct,'sitting': self.sitting,}
        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)
