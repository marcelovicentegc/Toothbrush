from django.urls import re_path
from toothpaste.views import IndexView, AboutView, ResultView, ChartData



urlpatterns = [
    re_path(r'^$', IndexView.as_view()),
    re_path(r'^api/chart/data/$', ChartData.as_view()),
    re_path(r'^result/$', ResultView.as_view()),
    re_path(r'^about/$', AboutView.as_view()),
]

# (?P<pk>\d+)/