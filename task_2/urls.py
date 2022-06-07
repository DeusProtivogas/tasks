
from django.urls import path
from task_2.views import TaskGuessingView, TaskGuessingViewStart, TaskGuessedCorrectlyView


urlpatterns = [
    path("", TaskGuessingView.as_view(), name="guess"),
    path("<int:id>/", TaskGuessingViewStart.as_view(), name="new_guess"),
    path("correct/", TaskGuessedCorrectlyView.as_view(), name="correct"),
]
