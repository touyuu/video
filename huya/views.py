from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import redirect

from huya.huya import Huya


def index(request, id):
    #return HttpResponse("Hello, world. You're at the polls index.")

    s = Huya(id)
    return redirect(s.get_real_url(id), permanent=True)