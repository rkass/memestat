import sys
import os
from django.core.management import setup_environ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

print "Classified: " + str(Meme.objects.filter(classification = None).count())
print "Unclassified: " + str(Meme.objects.filter(classification != None).count())
