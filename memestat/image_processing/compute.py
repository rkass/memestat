import Image
import math
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import s3

#performs side effex on im1
def merge(im1, img2, x): 
  i1 = im1.load()
  img2 = img2.resize(im1.size)
  i2 = img2.load()
  for x in range(img2.size[0]):
    for y in range(img2.size[1]):
      i1[x, y] = ((i1[x, y][0]*x + i2[x, y][0]) / (x + 1), 
              (i1[x, y][1]*x + i2[x, y][1]) / (x + 1),(i1[x, y][2]*x + i2[x, y][2]) / (x + 1))

def oneDPearsonHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((16, 16), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  i1 = img1.load()
  i2 = img2.load()
  xtot, ytot = 0., 0.
  iters = 0
  for x in range(width):
    for y in range(height):
      first = i1[x, y]
      second = i2[x, y]
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      if first != (255, 255, 255) and first != (0, 0, 0):
        xtot += first[0] + first[1] + first[2]
        ytot += second[0] + second[1] + second[2]
        iters += 1
  xm = xtot / iters
  ym = ytot / iters
  num, denom0, denom1 = 0., 0., 0.
  for x in range(width):
    for y in range(height):
      first = i1[x, y]
      second = i2[x, y]
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      xi = first[0] + first[1] + first[2]
      yi = second[0] + second[1] + second[2]
      num += (xi - xm) * (yi - ym)
      denom0 += (xi - xm)**2
      denom1 += (yi - ym)**2
  return num / (math.sqrt(denom0) * math.sqrt(denom1))

def rawDistanceHelp(img1, img2):
  initWidth, initHeight = img1.size
  img1 = img1.resize((8, 8), Image.BILINEAR)
  width, height = img1.size
  img2 = img2.resize((width, height), Image.BILINEAR)
  i1 = img1.load()
  i2 = img2.load()
  distance = 0.0
  iters = 0.0
  for x in range(width):
    for y in range(height):
      first = i1[x, y]
      second = i2[x, y]
      if isinstance(first, int):
        first = (first, first, first)
      if isinstance(second, int):
        second = (second, second, second)
      if True:#first != (255, 255, 255):
        distance += math.sqrt((first[0] - second[0])**2 +
          (first[1] - second[1])**2 + (first[2] - second[2])**2)
        iters += 1
  return distance/iters

#cuts image into (width, height * .4) at centerpoint
def centerCut(im):
  midpoint= int(im.size[1]/2); # hight
  points = (0, (midpoint - int(.15*im.size[1])), im.size[0], (midpoint + int(.15 *im.size[1]))) 
  cropped = im.crop(points);
  return cropped;

def distanceTop(target, bucket):
  best = sys.maxint
  bestKey = ""
  count = 0
  for k, v in s3.getImgs(bucket).items():
    thisDist = rawDistanceHelp(target, centerCut(v))
    if thisDist < best:
      best = thisDist
      bestKey = k
    count += 1
  return (bestKey, best, count)

def correlationTop(target, bucket):
  best = -1
  bestKey = ""
  count = 0
  for k, v in s3.getImgs(bucket).items():
    thisCorrelation = oneDPearsonHelp(target, centerCut(v))
    if thisCorrelation > best:
      best = thisCorrelation
      bestKey = k
    count += 1
  return (bestKey, best, count)
