import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import control
import settings
import s3
from collections import Counter
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import *

#There was a bug in control.classify where macros were being created too easily, this breaks those up
#that were created too easily

macros = ImageMacro.objects.all()

for macro in macros:
  memes = Meme.objects.filter(classification = macro)
  if len(memes) == 2:
    fst = memes[0]
    snd = memes[1]
    if fst.topDist >= 14 and snd.topDist >= 14:
      print "Decoupling..."
      print fst.threadLink
      print snd.threadLink
      fst.delete()
      snd.delete()
      s3.delete('macros', macro.key)
      macro.delete()
