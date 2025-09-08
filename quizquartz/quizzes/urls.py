from django.urls import path
from .views import (
    TagListAPIView,
    QuizGroupListAPIView,
    QuizGroupDetailAPIView,
    QuizListAPIView,
    QuizDetailAPIView,
    QuizGroupCreateAPIView,
    QuizGroupUpdateAPIView,
    QuizGroupDeleteAPIView,
    QuizCreateAPIView,
    QuizUpdateAPIView,
    QuizDeleteAPIView,
)


urlpatterns = [
    # Any user can access.
    path(route="tag/", view=TagListAPIView.as_view()),
    path(route="quizgroup/", view=QuizGroupListAPIView.as_view()),
    path(route="quizgroup/<uuid:pk>/", view=QuizGroupDetailAPIView.as_view()),
    path(route="quiz/", view=QuizListAPIView.as_view()),
    path(route="quiz/<uuid:pk>/", view=QuizDetailAPIView.as_view()),
    # Authenticated users only can access.
    path(route="quizgroup/create/", view=QuizGroupCreateAPIView.as_view()),
    path(route="quizgroup/<uuid:pk>/update/", view=QuizGroupUpdateAPIView.as_view()),
    path(route="quizgroup/<uuid:pk>/delete/", view=QuizGroupDeleteAPIView.as_view()),
    path(route="quiz/create/", view=QuizCreateAPIView.as_view()),
    path(route="quiz/<uuid:pk>/update/", view=QuizUpdateAPIView.as_view()),
    path(route="quiz/<uuid:pk>/delete/", view=QuizDeleteAPIView.as_view()),
]
