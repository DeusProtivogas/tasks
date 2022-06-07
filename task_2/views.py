from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class TaskGuessingViewStart(View):
    def get(self, request, id):
        # Провека на правильность номера
        if id < 0 or id > 100:
            return JsonResponse({
                "ans": f"Введен неправильный номер предмета",
            }, status=400)
        # Пока не известно больше про вероятность, id предмета не должен влиять на его цвет
        request.session['guesses'] = 0
        # Угадываем все варианты в порядке вероятности выпадания варианта
        request.session['variants'] = ["Синий", "Зеленый", "Красный"]

        return redirect("guess")

@method_decorator(csrf_exempt, name="dispatch")
class TaskGuessingView(View):
    """
    Угадываю цвет, увеличиваю число попыток, пока не угадаю (или не закончатся цвета)
    """
    def get(self, request):
        guesses = request.session.get("guesses")

        request.session['guesses'] = guesses

        return render(
            request,
            'task_2.html',
            context={"guesses_total": guesses, "guess": request.session['variants'][guesses]},
        )

    def post(self, request):
        guesses = request.session.get("guesses")
        if 'NO' in request.POST:
            guesses += 1

        request.session['guesses'] = guesses
        if request.session.get("guesses") >= 3:
            return JsonResponse({
                "ans": f"Как-то получилось, что не угадал",
            }, status=200)

        return redirect("guess")


@method_decorator(csrf_exempt, name="dispatch")
class TaskGuessedCorrectlyView(View):
    def get(self, request):
        """
        Возвращаем подсчет попыток, за которые угадали
        """
        return JsonResponse({
            "ans": f"Угадал за {request.session.get('guesses') + 1} попыток",
        }, status=200)