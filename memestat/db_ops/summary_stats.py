import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
#from django.core.management import setup_environ
#setup_environ(settings)
from stats.models import *

def topMacro():
  mod, ds = ImageMacro.objects.memeOfTheDay()
  hs = tallyScore(mod, 
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 1))
  ths = tallyScore(mod,
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 2),
        upperLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 1))
  tds = tallyScore(mod,
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 48),
        upperLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 24))
  tm = TopMacro(dailyScore = ds, hourlyScore = hs)
  if ths != 0:
    tm.hourlyChange = int(round(((float(hs) / float(ths)) - 1)  * 100))
  if tds != 0:
    tm.dailyChange = int(round(((float(ds) / float(tds)) - 1) * 100))
  tm.save()
  for macro in mod:
    tm.macros.add(macro)
  print "Top Macro created and stored with name: " + mod[0].name
  print "Daily Score: " + str(ds)
  print "Hourly Score: " + str(hs) 
  print "Daily Change: " + str(tm.dailyChange)
  print "Hourly Change: " + str(tm.hourlyChange)
  return tm
