from django.db import models
from django.utils.timezone import utc
from datetime import datetime, timedelta
from operator import itemgetter

#Takes a single macro group along with time constraints and outputs
#the score for that macro group for the given time constraints 
def tallyScore(group, 
  lowerLimit = datetime(2012, 5, 3, 17, 56, 17, 828221, tzinfo=utc),
  upperLimit = datetime.now().replace(tzinfo = utc)):
  score = 0
  for macro in group:
    memes = Meme.objects.filter(classification = macro, created_at__gte = lowerLimit, 
      created_at__lte = upperLimit)
    for meme in memes:
      score += meme.score
  return score
#Takes an entire set of macro groups along with time constraints and
#outputs an array of two-tuples of group, score sorted by the tuples
#with highest score first
def tallyScoresGroups(groups, 
  lowerLimit = datetime(2012, 5, 3, 17, 56, 17, 828221, tzinfo=utc),
  upperLimit = datetime.now().replace(tzinfo = utc)):
  returnSet = []
  for group in groups:
    returnSet.append((group, tallyScore(group, lowerLimit, upperLimit)))
  return sorted(returnSet, key = lambda tup: tup[1])[::-1]
#Takes a single macro group along with two time intervals and outputs the
#ratio of the score in interval one to the score of interval two
def tallyScoreInterval(group, lowerLimit1, upperLimit1, lowerLimit2, upperLimit2):
  score1 = 0.
  for macro in group:
    memes = Meme.objects.filter(classification = macro, created_at__gte = lowerLimit1, 
      created_at__lte = upperLimit1)
    for meme in memes:
      score1 += meme.score
  score2 = 0.
  for macro in group:
    memes = Meme.objects.filter(classification = macro, created_at__gte = lowerLimit2, 
      created_at__lte = upperLimit2)
    for meme in memes:
      score2 += meme.score
  if score2 == 0:
    return score1
  return float(score1) / float(score2)

def tallyScoreGroupRatio(group, lowerLimit, upperLimit):
  lastDay = tallyScore(group, lowerLimit, upperLimit)
  forevs = tallyScore(group, upperLimit = lowerLimit)
  return float(lastDay) / float(forevs)

def tallyScoresGroupsDailyRatio(groups):
  lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(days = 1)
  upperLimit = datetime.utcnow().replace(tzinfo = utc)
  returnSet = []
  for group in groups:
    returnSet.append((group, tallyScoreGroupRatio(group, lowerLimit, upperLimit)))
  return sorted(returnSet, key = lambda tup: tup[1])[::-1]

#Takes an entire set of macro groups along with two sets of time contraints and
#outputs an array of two-tuples of group, ratio of score of first interval to
#score of second interval.
def tallyScoresGroupsInterval(groups, lowerLimit1, upperLimit1, lowerLimit2, upperLimit2):
  returnSet = []
  for group in groups:
    returnSet.append((group, tallyScoreInterval(group, lowerLimit1, upperLimit1,
      lowerLimit2, upperLimit2)))
  return sorted(returnSet, key = lambda tup: tup[1])[::-1]

class MacroGrouper(models.Manager):
  def group(self):
    allMacros = self.all().order_by('name')
    lastName = ''
    returnSet = []
    for macro in allMacros:
      if macro.name == '' or lastName != macro.name:
        returnSet.append([macro])
      else:
        returnSet[-1].append(macro)
      lastName = macro.name
    return returnSet
  #returns the highest scoring memegroup for the last 24 hours along with score in a tuple
  def memeOfTheDay(self):
    return tallyScoresGroups(self.group(), 
      lowerLimit = datetime.utcnow().replace(tzinfo = utc) - timedelta(days = 1))[0]
  #daily
  def shootingStar(self):
    ll1 = datetime.utcnow().replace(tzinfo = utc) - timedelta(days = 1)
    return tallyScoresGroupsInterval(self.group(), ll1, datetime.now().replace(tzinfo = utc),
      datetime.utcnow().replace(tzinfo = utc) - timedelta(days = 2), ll1)[0]
  def sinkingStone(self):
    ll1 = datetime.utcnow().replace(tzinfo = utc) - timedelta(days = 1)
    return tallyScoresGroupsInterval(self.group(), ll1, datetime.now().replace(tzinfo = utc),
      datetime.utcnow().replace(tzinfo = utc) - timedelta(days = 2), ll1)[::-1][0]
  def shootingStar2(self):
    return tallyScoresGroupsDailyRatio(self.group())[0]
  def sinkingStone2(self):
    return tallyScoresGroupsDailyRatio(self.group())[::-1][0]


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
