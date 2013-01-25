import sys
import os
from django.core.management import setup_environ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

classified = Meme.objects.filter(classification = None).count()
print "Classified: " + str(classified)
print "Unclassified: " + str(Meme.objects.all() - classified)
