import Image
import urllib3
import json
import cStringIO as cS
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import settings
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'image_processing')))
import control
from django.core.management import setup_environ
setup_environ(settings)

def fullSizePhoto(url):
  page = urllib3.PoolManager().request('GET', url)._body
  pageRev = page[:(page.find('.jpg') + 4)][::-1]
  return pageRev[:pageRev.find('=') - 1][::-1]

page = 'http://reddit.com/r/adviceanimals.json'
goDeeper = True #stop burrowing when we encounter a page with no posts over a score of 25
while(goDeeper):
  goDeeper = False
  try: pageJson = json.loads(urllib3.PoolManager().request('GET', page).data)
  except: continue
  for post in pageJson['data']['children']:
    if post['data']['score'] > 10:
      goDeeper = True
      if ".jpg" in post['data']['url'] or  ".png" in post['data']['url'] or ".jpeg" in post['data']['url']:
        fullSizeLink = post['data']['url']
      else:
        fullSizeLink = fullSizePhoto(post['data']['url'])
      try:
        target = Image.open(cS.StringIO(urllib3.PoolManager().request('GET', fullSizeLink).data)).convert('RGB')
      except: target = None
      if target != None:
        postDict = {'threadLink' : 'http://reddit.com' + post['data']['permalink'],
          'thumbnailLink' : post['data']['thumbnail'], 'fullSizeLink' : 
          fullSizeLink, 'score' : post['data']['score'], 'created' : post['data']['created'],
          'author' : post['data']['author'], 'source' : 'r/adviceanimals'}
        control.processItem(postDict, target)
  lastId = pageJson['data']['after']
  page = 'http://reddit.com/r/adviceanimals.json?after=' + lastId
  print "On to the next"

