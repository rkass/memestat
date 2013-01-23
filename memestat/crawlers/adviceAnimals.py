import Image
import urllib3
import json
import cStringIO as cS
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
import s3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import classify
import compute
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro

def fullSizePhoto(url):
  page = urllib3.PoolManager().request('GET', url)._body
  pageRev = page[:(page.find('.jpg') + 4)][::-1]
  return pageRev[:pageRev.find('=') - 1][::-1]

##sets oldest pim to inactive and removes it from s3 if necessary
##adds new pim to s3
def potentialize(threadLink, target):
  pims = PotentialImageMacros.objects.filter(active = True).order_by('created_at')
  if pims.count() > 500:
    #deactivate the oldest pim
    s3.delete('potentialmacros', pims[0].key)
    pims[0].active = False
  s3.add('potentialmacros', threadLink, target) 
  
def librarize(key):
  s3.add('macros', key, s3.getImg('potentialmacros', key))
  s3.delete('potentialmacros', key)
  pim = PotentialImageMacro.objects.get(key = key)
  pim.active = False
  im = ImageMacro.objects.create(key = key)
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
  if q.count() > 1:
    raise Exception("More than one of the same permalink in db for permalink:" + data['permalink'])
  if q.count() == 1:
    #if we have, update the score and move on
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
        p = PotentialImageMacro(thumbnailLink = arr['thumbnail'], fullSizeLink = arr['fullSizeLink'],
          score = arr['score'], submitter = arr['author'], source = arr['source'], created = arr['created']
          , threadLink = arr['threadLink'], key = arr['threadlink'])
        p.save()
        potentialize(data['threadlink'], target)
      elif classification2[2] < 20: #only classify as potential if very confident
        librarize(classification[0])
        macro = ImageMacro.objects.get(key = classification[0])
        if classification[1] < 25: merge(classification[0], macro)
      #Unaddressed case: weak classification.  Do not want to classify as potential because
      #doing sois going out on a limb without strong reason to do so.  Also do not want to
      #add it as a potential macro because it is likely reduntant.  
    #Image must be corrput because a value was not attained for closest with distance
    elif classification[1] == None:
      macro = None
      img_corrupt = True
    else:
      macro = ImageMacro.objects.get(key = classification[0])
      if classification[1] < 25: merge(classification[0], macro)
    m = Meme(classification = macro, thumbnailLink = arr['thumbnailLink'],
          fullSizeLink = arr['fullSizeLink'], score = arr['score'], submitter = arr['author'],
          topDist = classification[1] , topCorr = classification[2] ,
          source = arr['source'], created = arr['created'], threadLink = arr['threadLink'],
          img_corrupt = img_corrupt)
    m.save()

page = 'http://reddit.com/r/adviceanimals.json'
goDeeper = True #stop burrowing when we encounter a page with no posts over a score of 25
while(goDeeper):
  goDeeper = False
  pageJson = json.loads(urllib3.PoolManager().request('GET', page).data)
  for post in pageJson['data']['children']:
    if post['data']['score'] > 25:
      goDeeper = True
      if (".jpg" or ".png") in post['data']['url']:
        fullSizeLink = post['data']['url']
      else:
        fullSizeLink = fullSizePhoto(post['data']['url'])
      target = Image.open(cS.StringIO(urllib3.PoolManager().request('GET', fullSizeLink).data))
      postDict = {'threadLink' : 'http://reddit.com' + post['data']['permalink'],
        'thumbnailLink' : post['data']['thumbnail'], 'fullSizeLink' : fullSizeLink,
        'created' : post['data']['created'], 'source' : 'r/adviceanimals'}
      processItem(postDict, target)
  lastId = pageJson['data']['after']
  page = 'http://reddit.com/r/adviceanimals.json?after=' + lastId
  print "On to the next"

