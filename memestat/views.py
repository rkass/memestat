from django.shortcuts import render_to_response
from django.template import RequestContext
from stats.models import *

def home(request):
  topMeme = TopMacro.objects.latest('id')
  sinkingStone = TopMacro.objects.latest('id')
  shootingStar = TopMacro.objects.latest('id')
  return render_to_response('home.html', {'shootingStar' : shootingStar}, context_instance=RequestContext(request))
