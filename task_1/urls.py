
from django.urls import path
from task_1.views import TaskQuadraticView

urlpatterns = [
    path("", TaskQuadraticView.as_view())
]
