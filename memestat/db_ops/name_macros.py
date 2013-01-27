sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import image_processing.control
import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

macros = ImageMacro.objects.all()
for macro in macros:
  fullSize = Meme.objects.filter(classification = macro)[0].fullSizeLink
  macro.name = image_processing.control.name(fullSize)
  macro.save()
