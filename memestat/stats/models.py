from django.db import models

class ImageMacro(models.Model):
  key = models.CharField(max_length = 1000)
  name = models.CharField(max_length = 1000, null = True)
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
