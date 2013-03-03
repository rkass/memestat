from django.db import models
from django.utils.timezone import utc
from datetime import datetime, timedelta
from operator import itemgetter

#Takes a single macro group along with two time intervals and outputs the
#ratio of the score in interval one to the score of interval two
class MacroGrouper(models.Manager):
  def group(self):
    allMacros = self.all().order_by('name')
    lastName = ''
    returnSet = []
    for macro in allMacros:
      if macro.name == '' or macro.name == None or lastName != macro.name:
        returnSet.append([macro])
      else:
        returnSet[-1].append(macro)
      lastName = macro.name
    return returnSet
  #Takes a single macro group along with time constraints and outputs
  #the score for that macro group for the given time constraints 
  def tallyScore(self,group, 
    lowerLimit = datetime(2012, 5, 3, 17, 56, 17, 828221, tzinfo=utc),
    upperLimit = datetime.now().replace(tzinfo = utc)):
    score = 0
    for macro in group:
      memes = Meme.objects.filter(classification = macro, created_at__gte = lowerLimit, 
        created_at__lte = upperLimit).distinct()
    for meme in memes:
      score += meme.score
    return score
  #Takes an entire set of macro groups along with time constraints and
  #outputs an array of two-tuples of group, score sorted by the tuples
  #with highest score first
  def tallyScoresGroups(self, groups, 
    lowerLimit = datetime(2012, 5, 3, 17, 56, 17, 828221, tzinfo=utc),
    upperLimit = datetime.now().replace(tzinfo = utc)):
    returnSet = []
    for group in groups:
      returnSet.append((group, self.tallyScore(group, lowerLimit, upperLimit)))
    return sorted(returnSet, key = lambda tup: tup[1])[::-1]
  #returns the points per day of the group for the last n days
  def nDayAverage(self, group, n):
    score = self.tallyScore(group, lowerLimit = datetime.utcnow().replace(tzinfo = utc) - 
      timedelta(hours = 24 * n))
    return float(score) / n
  #returns nDayAverage / lastDay, someNumber.  if it's an infinite ratio,
  #someNumber = lastDay and use None to rep infinity, anything else someNumber = lastDay
  def nDayAverageRatio(self, group, n):
    nDayAverage = float(self.nDayAverage(group, n))
    lastDay = float(self.tallyScore(group, lowerLimit = datetime.utcnow().replace(tzinfo = utc) -
      timedelta(hours = 24)))
    if lastDay == 0:
      return (None, nDayAverage)
    else:
      return (nDayAverage / lastDay, lastDay)
  def nDayAverageRatioGroups(self, groups, n):
    ret = []
    for group in groups:
      ratio, someNumber = self.nDayAverageRatio(group, n)
      ret.append((group, ratio, someNumber))
    return  sorted(ret, key = lambda tup: tup[1])
  def sinkingStone(self):
    nones = []
    macros = self.nDayAverageRatioGroups(self.group(), 3)[::-1]
    newNone = macros.pop()
    while(newNone[1] == None):
      nones.append(newNone)
      newNone = macros.pop()
    if len(nones) == 0:
      return newNone
    return max(nones, key = lambda x:x[2])
  def shootingStar(self):
    zeros = []
    macros = self.nDayAverageRatioGroups(self.group(), 3)[::-1]
    newZero = macros.pop()
    while(newZero[1] <= 0):
      if newZero[1] == 0:
        zeros.append(newZero)
      newZero = macros.pop()
    if len(zeros) == 0:
      return newZero
    return max(zeros, key = lambda x:x[2])
  #returns the highest scoring memegroup for the last 24 hours along with score in a tuple
  def memeOfTheDay(self):
    return self.tallyScoresGroups(self.group(), 
      lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(hours = 24))[0]
 
class ImageMacro(models.Model):
  key = models.CharField(max_length = 1000)
  name = models.CharField(max_length = 1000, null = True)
  objects = MacroGrouper()
##For the next two models, created refers to thread creation,
##and created_at refers to object creation

class Meme(models.Model):
  classification = models.ForeignKey(ImageMacro, null = True, related_name = 'classification')
  thumbnailLink = models.URLField()
  fullSizeLink = models.URLField()
  score = models.IntegerField(null = True)
  submitter = models.CharField(max_length = 200, null = True)
  topCorr = models.FloatField(null = True)
  topDist = models.FloatField(null = True)
  source = models.CharField(max_length = 200)
  created = models.IntegerField()
  threadLink = models.URLField()
  created_at = models.DateTimeField(auto_now_add = True)
  img_corrupt = models.BooleanField()
  name = models.CharField(max_length = 1000, null = True)

class PotentialImageMacro(models.Model):
  key = models.CharField(max_length = 1000)
  thumbnailLink = models.URLField()
  fullSizeLink = models.URLField()
  score = models.IntegerField(null = True)
  submitter = models.CharField(max_length = 200, null = True)
  source = models.CharField(max_length = 200)
  created = models.IntegerField()
  threadLink = models.URLField()
  created_at = models.DateTimeField(auto_now_add = True)
  active = models.BooleanField(default = True)

#changes are percent values rounded to the nearest integer
class TopMacro(models.Model):
  macros = models.ManyToManyField(ImageMacro)
  dailyScore = models.IntegerField()
  hourlyScore = models.IntegerField()
  dailyChange = models.IntegerField(null = True)
  hourlyChange = models.IntegerField(null = True)
  created_at = models.DateTimeField(auto_now_add = True)

class ShootingStar(models.Model):
  macros = models.ManyToManyField(ImageMacro)
  dailyScore = models.IntegerField()
  hourlyScore = models.IntegerField()
  dailyChange = models.IntegerField(null = True)
  hourlyChange = models.IntegerField(null = True)
  created_at = models.DateTimeField(auto_now_add = True)

class SinkingStone(models.Model):
  macros = models.ManyToManyField(ImageMacro)
  dailyScore = models.IntegerField()
  hourlyScore = models.IntegerField()
  dailyChange = models.IntegerField(null = True)
  hourlyChange = models.IntegerField(null = True)
  created_at = models.DateTimeField(auto_now_add = True)
