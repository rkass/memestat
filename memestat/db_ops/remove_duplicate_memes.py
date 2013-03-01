import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import control
import settings
from collections import Counter
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import *

memes = Meme.objects.all().distinct().order_by('threadLink')
last = memes[0].threadLink
cnt = 1
while cnt < memes.count():
  tmp = memes[cnt].threadLink
  if memes[cnt].threadLink == last:
    memes[cnt].delete()
    print "Duplicate meme deleted"
  last = tmp
  cnt += 1
