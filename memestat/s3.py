import boto
import sys
import cStringIO as cS
import Image
sys.path.append("..")
import aws_credentials

conn = boto.connect_s3(aws_credentials.key, aws_credentials.secret)

#returns a set of key values with key key and value it's corresponding image
def getImgs(bkt):
  retDict = {}
  bucket = conn.get_bucket(bkt)
  keys = bucket.get_all_keys()
  for keyobj in keys:
    retDict[keyobj.key] = Image.open(cS.StringIO(keyobj.read()))
  return retDict

def getPotentials():
  return getImgs('potentialmacros')

def getMacros():
  return getImgs('macros')
