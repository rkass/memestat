import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import *

def computeStats(group):
  ds = ImageMacro.objects.tallyScore(group,
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 24))
  hs = ImageMacro.objects.tallyScore(group, 
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 1))
  ths = ImageMacro.objects.tallyScore(group,
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 2),
        upperLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 1))
  tds = ImageMacro.objects.tallyScore(group,
        lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 48),
        upperLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 24))
  tm = TopMacro(dailyScore = ds, hourlyScore = hs)
  hc = None
  if ths != 0:
    hc = int(round(((float(hs) / float(ths)) - 1)  * 100))
  dc = None
  if tds != 0:
    dc = int(round(((float(ds) / float(tds)) - 1) * 100))
  return (ds, hs, dc, hc)


def topMacro():
  mod = ImageMacro.objects.memeOfTheDay()[0]
  (ds, hs, dc, hc) = computeStats(mod)
  tm = TopMacro(dailyScore = ds, hourlyScore = hs)
  if dc != None:
    tm.dailyChange = dc
  if hc != None:
    tm.hourlyChange = hc
  tm.save()
  for m in mod:
    tm.macros.add(m)
  print "Top Macro created and stored with name: " + str(mod[0].name)
  print "Daily Score: " + str(ds)
  print "Hourly Score: " + str(hs) 
  print "Daily Change: " + str(tm.dailyChange)
  print "Hourly Change: " + str(tm.hourlyChange)
  return tm

def sinkingStone():
  group = ImageMacro.objects.sinkingStone()[0]
  ds, hs, dc, hc = computeStats(group)
  ss = SinkingStone(dailyScore = ds, hourlyScore = hs) 
  if dc != None:
    ss.dailyChange = dc
  if hc != None:
    ss.hourlyChange = hc
  ss.save()
  for g in group:
    ss.macros.add(g)
  print "Sinking Stone created and stored with name: " + str(group[0].name)
  print "Daily Score: " + str(ds)
  print "Hourly Score: " + str(hs)
  print "Daily Change: " + str(ss.dailyChange)
  print "Hourly Change: " + str(ss.hourlyChange)
  return ss

def shootingStar():
  group = ImageMacro.objects.shootingStar()[0]
  ds, hs, dc, hc = computeStats(group)
  ss = ShootingStar(dailyScore = ds, hourlyScore = hs)
  if dc != None:
    ss.dailyChange = dc
  if hc != None:
    ss.hourlyChange = hc
  ss.save()
  for g in group:
    ss.macros.add(g)
  print "Shooting Star created and stored with name: " + str(group[0].name)
  print "Daily Score: " + str(ds)
  print "Hourly Score: " + str(hs)
  print "Daily Change: " + str(ss.dailyChange)
  print "Hourly Change: " + str(ss.hourlyChange)
  return ss
