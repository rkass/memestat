import boto
import sys, os
import cStringIO as cS
import StringIO as s
import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import aws_credentials
from boto.s3.connection import Key

conn = boto.connect_s3(aws_credentials.key, aws_credentials.secret)

#returns a set of key values with key key and value it's corresponding image
def getImgs(bkt):
  retDict = {}
  bucket = conn.get_bucket(bkt)
  keys = bucket.get_all_keys()
  for keyobj in keys:
    try: 
      i = Image.open(cS.StringIO(keyobj.read()))
      retDict[keyobj.key] = i
    except:
      print "Couldn't find " keyobj.key
  return retDict

def getPotentials():
  return getImgs('potentialmacros')

def getMacros():
  return getImgs('macros')

def delete(bkt, key):
  bucket = conn.get_bucket(bkt)
  keyobj = bucket.get_key(key)
  keyobj.delete()

def add(bkt, key, img, form = 'JPEG'):
  bucket = conn.get_bucket(bkt)
  newKeyObj = Key(bucket)
  newKeyObj.key = key
  buf = s.StringIO()
  img.save(buf, form)
  newKeyObj.set_contents_from_string(buf.getvalue())

def getImg(bkt, key):
  bucket = conn.get_bucket(bkt)
  keyobj = bucket.get_key(key)
  return Image.open(cS.StringIO(keyobj.read()))

def replace(bkt, key, img, form = 'JPEG'):
  bucket = conn.get_bucket(bkt)
  keyobj = bucket.get_key(key)
  buf = s.StringIO()
  img.save(buf, form)
  keyobj.set_contents_from_string(buf.getvalue())
