from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from fallServer.models import FormatedData, FallId

import numpy as np
import mlpy
import matplotlib.pyplot as plt 

import PIL
import PIL.Image
import StringIO
def index(request):
	# data = FormatedData.objects.all().order_by('id')[:50]
	FallIdData = FallId.objects.all().order_by('id')[:]
	
	context = {'FallIdData': FallIdData}
	return render(request, 'index.html', context)

def detail(request, poll_id):
	return HttpResponse("You're looking at poll {id}.".format(id = poll_id))

def results(request, poll_id):
	return HttpResponse("You're looking at the results of poll {id}.".format(id = poll_id))

def vote(request, poll_id):
	return HttpResponse("You're voting on poll {id}.".format(id = poll_id))
