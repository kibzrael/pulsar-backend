from django.urls import path

from reports.inappropriate import InappropriateView
from reports.issues import IssuesView

urlpatterns = [
    path("issues", IssuesView.as_view()),
    path("inappropriate", InappropriateView.as_view()),
]
