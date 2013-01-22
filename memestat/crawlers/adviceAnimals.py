import merge as m
import shutil
import os
import urllib3
import json
import settings
import sys
sys.path.append("..")
import image_processing.classify as classify
from django.core.management import setup_environ
setup_environ(settings)
from stats.models import ImageMacro
from stats.models import Meme
from stats.models import PotentialImageMacro
import Image
dropBoxDir = str.strip(open('../dropBoxDir', 'r').read())

def fullSizePhoto(url):
  page = urllib3.PoolManager().request('GET', url)._body
  pageRev = page[:(page.find('.jpg') + 4)][::-1]
  return pageRev[:pageRev.find('=') - 1][::-1]

def oldestFileInTree(rootfolder, extension = ".jpg"):
    return min(
        (os.path.join(dirname, filename)
        for dirname, dirnames, filenames in os.walk(rootfolder)
        for filename in filenames
        if filename.endswith(extension)),
        key=lambda fn: os.stat(fn).st_mtime)
##here
def potentialize(permalink):
  if len(os.listdir(dropBoxDir + 'potential_libs/')) > 500:
    #delete a potential lib before adding this one
    os.remove(oldestFileInTree(dropBoxDir + 'potential_libs/')) 
  shutil.copyfile(dropBoxDir + 'target.jpg', dropBoxDir + 'potential_libs/' + permalink + '.jpg')

def librarize(fileName):
  print fileName
  shutil.copyfile(dropBoxDir + 'potential_libs/' + fileName, dropBoxDir + 'library/' + fileName)
  os.remove(dropBoxDir + 'potential_libs/' + fileName)
  pim = PotentialImageMacro.objects.get(title = fileName)
  im = ImageMacro.objects.create(filename = 'library/' + fileName)
  m = Meme.objects.get(threadLink = pim.threadLink)
  m.classification = im
  m.topdist = 0
  m.strong_classification = True
  m.save()
  pim.delete()

def merge(lib_img_path, macro, detract = 0):
  libimg = Image.open(dropBoxDir + lib_img_path)
  targimg = Image.open(dropBoxDir + 'target.jpg')
  backedby = Meme.objects.filter(classification = macro).count()
  m.merge(libimg, targimg, backedby - detract)
  if ".jpg" not in (dropBoxDir + lib_img_path):
    libimg.save(dropBoxDir + lib_img_path + ".jpg")
  libimg.save(dropBoxDir + lib_img_path)

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
    c2 = False #variable determining if the image was classified according to a potential or established macro
    #classify.classify() gets 2 elements: image macro/none, strong/weak
    classification = classify.classify(target, 'macros') 
    if classification[0] == None and classification[1] != None:
      c2 = True
      macro = None
      #try classifying on potential libs
      classification2 = classify.classify(target, 'potentialmacros')
      if classification2[0] == None:
        #add image to potential_libs
        p = PotentialImageMacro(thumbnailLink = arr['thumbnail'], fullSizeLink = arr['fullSizeLink'],
          score = arr['score'], submitter = arr['author'], source = arr['source'], created = arr['created']
          , threadLink = arr['threadLink'], key = arr['threadlink'])
        p.save()
        potentialize(data['threadlink'])
      elif classification2[2] < 20: #only classify as potential_lib if very confident
        librarize(classification2[0][8:])
        macro = ImageMacro.objects.get(filename = 'library/' + classification2[0][8:])
        print "Added " + classification2[0][8:] + " to the library while classifying: " + fullSize
        classification = classification2
    elif classification[2] == None:
      macro = None
      img_corrupt = True
    else:
      macro = ImageMacro.objects.get(filename = classification[0])
    m = Meme(classification = macro, thumbnailLink = data['thumbnail'],
          fullSizeLink = fullSize, score = data['score'], submitter = data['author'],
          topDist = classification[2] , topCorr = classification[3] ,
          source = 'adviceanimals', created = data['created'], threadLink = 'http://reddit.com' + data['permalink'],
          strong_classification = classification[1], img_corrupt = img_corrupt)
    m.save()
    if classification[2] < 25 and classification[0] != None:
      if c2: merge(classification[0], macro, detract = 1)
      else: merge(classification[0], macro)

if ".jpeg" not in data['url']:
    #have not evaluated this submission yet, run tests and store
    filepath = dropBoxDir + 'target.jpg'
    if ".jpg" in data['url'] or ".png" in data['url']:
      fullSize = data['url']
    else:
      fullSize = fullSizePhoto(data['url'])
    f = open(filepath, 'wb')
    f.write(urllib3.PoolManager().request('GET', fullSize).data)
    f.close()
    img_corrupt = False
    c2 = False
page = 'http://reddit.com/r/adviceanimals.json'
goDeeper = True #stop burrowinandwhen we encounter a page with no posts over a score of 25
while(goDeeper):
  goDeeper = False
  pageJson = json.loads(urllib3.PoolManager().request('GET', page).data)
  for post in pageJson['data']['children']:
    if post['data']['score'] > 25:
      goDeeper = True
      processItemFullSize(post)
  lastId = pageJson['data']['after']
  page = 'http://reddit.com/r/adviceanimals.json?after=' + lastId
  print "On to the next"

