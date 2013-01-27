import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import control
import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

macros = ImageMacro.objects.all()
for macro in macros:
  fullSize = Meme.objects.filter(classification = macro)[0].fullSizeLink
  name = control.name(fullSize)
  macro.name = control.name(fullSize)
  macro.save()
  print "Named " + macro.key + " as " + name
