from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect

from douyu.douyu import DouYu


def index(request, id):
    #return HttpResponse("Hello, world. You're at the polls index.")

    s = DouYu(id)
    return redirect(s.get_js(), permanent=True)