try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from . import views

urlpatterns = [

    url(r'^$', view=views.QuizListView.as_view(),name='quiz_index'),
    url(r'^profile/(?P<pk>\d+)/$', view=views.QuizProfileView.as_view(), name='quiz_profile'),
    url(r'^quiz-welcome/$', view=views.QuizWelcomeView, name='quiz_welcome'),
    url(r'^progress/$', view=views.QuizUserProgressView.as_view(), name='quiz_progress'),
    url(r'^marking/$', view=views.QuizMarkingList.as_view(), name='quiz_marking'),
    url(r'^marking/(?P<pk>[\d.]+)/$', view=views.QuizMarkingDetail.as_view(), name='quiz_marking_detail'),
    url(r'^(?P<slug>[\w-]+)/$', view=views.QuizDetailView.as_view(), name='quiz_start_page'),
    url(r'^(?P<quiz_name>[\w-]+)/take/$', view=views.QuizTake.as_view(), name='quiz_question'),
    url(r'^(?P<quiz_name>[\w-]+)/take/(?P<question_number>\d+)/$', view=views.QuizTake.as_view(), name='quiz_question'),
]
