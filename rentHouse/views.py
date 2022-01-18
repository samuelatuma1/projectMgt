from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# Create your views here.
def index(request):
    return HttpResponse("Hello world")