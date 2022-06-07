import json
from math import sqrt

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

def calculate(a, b, c):
    """
    Подсчитывает количество корней и корни
    :return: Строка с ответом
    """
    d = b * b - (4 * a * c)  # Дискриминант
    if d < 0:
        return "No roots"
    if d > 0:
        x_1 = round((-b - sqrt(d)) / (2 * a), 2)
        x_2 = round((-b + sqrt(d)) / (2 * a), 2)
        return f"2 roots, {x_1}, {x_2}"
    x = round(-b / (2 * a))
    return f"1 root, {x}"


@method_decorator(csrf_exempt, name="dispatch")
class TaskQuadraticView(View):

    def get(self, request):

        a = request.GET.get("a")
        b = request.GET.get("b")
        c = request.GET.get("c")

        # Коэффициенты в URL
        try:
            ans = calculate(float(a), float(b), float(c))
            status = 200
        except:
            # Коэффициенты в теле
            data = json.loads(request.body)
            a = data.get("a")
            b = data.get("b")
            c = data.get("c")

            try:
                ans = calculate(float(a), float(b), float(c))
                status = 200
            except:
                # Не все переменные, либо неправильный тип переменных
                ans = "Loaded variables are incorrect"
                status = 400

        return JsonResponse({
            "answer": ans,
        }, status=status)
