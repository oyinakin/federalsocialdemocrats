from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone


def index(request):
    template = loader.get_template('fds_app/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def wherewestand(request):
    template = loader.get_template('fds_app/wherewestand.html')
    context = {}
    return HttpResponse(template.render(context, request))

def whoweare(request):
    template = loader.get_template('fds_app/whoweare.html')
    context = {}
    return HttpResponse(template.render(context, request))

def takeaction(request):
    template = loader.get_template('fds_app/takeaction.html')
    context = {}
    return HttpResponse(template.render(context, request))

def joiningpolitics(request):
    template = loader.get_template('fds_app/joiningpolitics.html')
    context = {}
    return HttpResponse(template.render(context, request))

def elections2023(request):
    template = loader.get_template('fds_app/2023elections.html')
    context = {}
    return HttpResponse(template.render(context, request))
