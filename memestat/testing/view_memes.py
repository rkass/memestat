import sys
import os
from django.core.management import setup_environ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

#Print all fullSizeLinks for an image macro with sys.argv in its key. Raise an error 
#if this snippet corresponds to more than one image macro key.
ims = ImageMacro.objects.all()
ioe = []
for i in ims:
  if sys.argv[1] in i.key:
    ioe.append(i)
if len(ioe) > 1:
  raise Exception("Too general of a string snippet--more than one corresponding macro")
memes = Meme.objects.filter(classification = ioe[0]).distinct()
for m in memes:
  print m.fullSizeLink
