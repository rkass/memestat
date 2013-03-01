import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import control
import settings
from collections import Counter
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

macros = ImageMacro.objects.all()
for macro in macros:
  cnt = Counter()
  memes = Meme.objects.filter(classification = macro).distinct()
  oldName = macro.name
  for m in memes:
    name = control.name(m.fullSizeLink)
    cnt[name] += 1
  macro.name = cnt.most_common()[0][0]
  macro.save()
  if oldName != macro.name:
    print "Renamed " + oldName + " to " + macro.name
  
