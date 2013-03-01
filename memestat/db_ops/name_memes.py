import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import control
import settings
from collections import Counter
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import *

cnt = 0
for meme in Meme.objects.all():
  meme.name = control.name(meme.fullSizeLink)
  meme.save() 
  print "Meme " + str(cnt) + " named " + meme.name  
  cnt += 1
