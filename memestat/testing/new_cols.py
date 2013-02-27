import sys 
import os
from django.core.management import setup_environ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro
from stats.models import TopMacro
from stats.models import SinkingStone
from stats.models import ShootingStar
for x in TopMacro.objects.all():
  x.delete()
for x in SinkingStone.objects.all():
  x.delete()
for x in ShootingStar.objects.all():
  x.delete()

x = 0
im = ImageMacro.objects.all()[0]
top = TopMacro(dailyChange = 3, hourlyChange = 1, dailyScore = 3, hourlyScore = 2)
top.save()
print "Top Macro successfully saved"
top.macros.add(im)
print "Top Macro successfully associated with an image macros"
if TopMacro.objects.all()[0].macros.all()[0] == im:
  print "Top Macro successfully fetched"
  x += 1
stone = SinkingStone(dailyChange = 3, hourlyChange = 1, dailyScore = 3, hourlyScore = 2)
stone.save()
print "Sinkning Stone successfully saved"
stone.macros.add(im)
print "Sinking Stone successfully associated with an image macros"
if SinkingStone.objects.all()[0].macros.all()[0] == im:
  print "Sinking Stone successfully fetched"
  x += 1
star = ShootingStar(dailyChange = 3, hourlyChange = 1, dailyScore = 3, hourlyScore = 2)
star.save()
print "Shooting Star successfully saved"
star.macros.add(im)
print "Shooting Star successfully associated with an image macros"
if ShootingStar.objects.all()[0].macros.all()[0] == im:
  print "Shooting Star successfully fetched"
  x += 1

top.delete()
star.delete()
stone.delete()
if TopMacro.objects.all().count() == SinkingStone.objects.all().count() == ShootingStar.objects.all().count == 0:
  print "All created records deleted, database back to normal"
else:
  print "Records not properly deleted"
  print TopMacro.objects.all().count()
  print SinkingStone.objects.all().count()
  print ShootingStar.objects.all().count()
if x == 3:
  print "All tests passed"
else:
  print "Some tests failed"




 
