from django.shortcuts import render

from django.http import HttpResponse

def main(request):
    return HttpResponse("OpenTASites / ")

def health(request):
    return HttpResponse("OpenTASites /health")
