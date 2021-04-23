try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from . import views

urlpatterns = [

    url(r'^$', view=views.QuizListView.as_view(),name='quiz_index'),
    url(r'^profile/', view=views.quizUserProfile(), name='quiz_user_profile'),
    url(r'^category/$', view=views.CategoriesListView.as_view(), name='quiz_category_list_all'),
    url(r'^category/(?P<category_name>[\w|\W-]+)/$', view=views.ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),
    url(r'^progress/$', view=views.QuizUserProgressView.as_view(), name='quiz_progress'),
    url(r'^marking/$', view=views.QuizMarkingList.as_view(), name='quiz_marking'),
    url(r'^marking/(?P<pk>[\d.]+)/$', view=views.QuizMarkingDetail.as_view(), name='quiz_marking_detail'),
    url(r'^(?P<slug>[\w-]+)/$', view=views.QuizDetailView.as_view(), name='quiz_start_page'),
    url(r'^(?P<quiz_name>[\w-]+)/take/$', view=views.QuizTake.as_view(), name='quiz_question'),
]
