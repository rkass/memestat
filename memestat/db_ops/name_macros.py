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
  oldName = macro.name
  control.updateName(macro)
