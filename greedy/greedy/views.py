from django.shortcuts import render
from django.shortcuts import render_to_response

from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
# Create your views here.

def greedy_view(request):

    print "====In HOME VIEW===="

    return HttpResponse("====In HOME VIEW====")
