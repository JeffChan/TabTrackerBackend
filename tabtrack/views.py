import urllib
import datetime
import math
import threading
import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect 
from django.conf import settings

def index(request):
    return HttpResponse("SSSSSSSSSSSUP")
