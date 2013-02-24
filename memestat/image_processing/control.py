import Image
import requests
import cStringIO as cS
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
import s3
import classify
import compute
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro
##sets oldest pim to inactive and removes it from s3 if necessary
##adds new pim to s3

def potentialize(threadLink, target):
  pims = PotentialImageMacro.objects.filter(active = True).order_by('created_at')
  if pims.count() > 500:
    print "Hey printing"
    #deactivate the oldest pim
    print pims[0].key
    print pims[0].created_at
    print pims[pims.count() - 1].key
    print pims[pims.count() - 1].created_at
    s3.delete('potentialmacros', pims[0].key)
    pims[0].active = False
  s3.add('potentialmacros', threadLink, target) 

#Try to name the library image by performing reverse google image search
def name(fullSizeLink):
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
  page = requests.get('http://www.google.com/searchbyimage?image_url=' + fullSizeLink, headers=headers).text
  page = page[page.find('Best guess for this image'):]
  page = page[page.find('>'):]
  return page[1 : page.find('<')]

  
def librarize(key):
  s3.add('macros', key, s3.getImg('potentialmacros', key))
  s3.delete('potentialmacros', key)
  pim = PotentialImageMacro.objects.get(key = key)
  pim.active = False
  im = ImageMacro.objects.create(key = key, name = name(pim.fullSizeLink))
  m = Meme.objects.get(threadLink = pim.threadLink)
  m.classification = im
  m.topdist = 0
  m.save()

def merge(macro, target):
  macroimg = s3.getImg('macros', macro.key)
  backedby = Meme.objects.filter(classification = macro).count()
  compute.merge(macroimg, target, backedby)
  s3.replace('macros', macro.key, macroimg)

def processItem(arr, target):
  q = Meme.objects.filter(threadLink = arr['threadLink'])
  #Have we evaluated this submission yet?  Might be worth considering only checking 
  #memes within the last day, or otherwise making the filter stronger
  print "Processing thread: " + arr['threadLink']
  if q.count() > 1:
    raise Exception("More than one of the same permalink in db for permalink:" + arr['permalink'])
  if q.count() == 1:
    #if we have, update the score and move on
    print "Repeat submission. Updating score and moving on..."
    m = q[0]
    m.score = arr['score']
    m.save()
  else:
    #have not evaluated this submission yet, run tests and store
    #classify.classify() gets 2 elements: image macro/none, strong/weak
    img_corrupt = False
    classification = classify.classify(target, 'macros') 
    if classification[0] == None and classification[1] != None:
      macro = None
      #try classifying on potential libs
      classification = classify.classify(target, 'potentialmacros')
      if classification[0] == None:
        #add image to potential_libs
        p = PotentialImageMacro(thumbnailLink = arr['thumbnailLink'], fullSizeLink = arr['fullSizeLink'],
          score = arr['score'], submitter = arr['author'], source = arr['source'], created = arr['created']
          , threadLink = arr['threadLink'], key = arr['threadLink'].replace('/', ''))
        p.save()
        potentialize(arr['threadLink'].replace('/', ''), target)
        print "Added as potential macro."
      elif classification[2] < 20: #only classify as potential if very confident
        librarize(classification[0])
        macro = ImageMacro.objects.get(key = classification[0])
        if classification[1] < 25: merge(macro, target)
        print "Moved " + classification[0] + " over to the library, and classified this item as such."
      #Unaddressed case: weak classification.  Do not want to classify as potential because
      #doing sois going out on a limb without strong reason to do so.  Also do not want to
      #add it as a potential macro because it is likely reduntant.  
    #Image must be corrput because a value was not attained for closest with distance
    elif classification[1] == None:
      print "Image corrupt"
      macro = None
      img_corrupt = True
    else:
      macro = ImageMacro.objects.get(key = classification[0])
      if classification[1] < 25: merge(macro, target)
      print "Classified as " + classification[0]
    m = Meme(classification = macro, thumbnailLink = arr['thumbnailLink'],
          fullSizeLink = arr['fullSizeLink'], score = arr['score'], submitter = arr['author'],
          topDist = classification[1] , topCorr = classification[2] ,
          source = arr['source'], created = arr['created'], threadLink = arr['threadLink'],
          img_corrupt = img_corrupt)
    m.save()
