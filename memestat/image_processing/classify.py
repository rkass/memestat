import compute as c

#Returns a classified image iff topDist < 40 or topDist == topCorr
def classify(target, bucket):
  try:
    target_crop = centerCut(target)
  except:
    return (None, None, None)
  topFileByDist, topDistVal = c.distanceTop(target_crop, bucket)
  if topDistVal < 40:
    return (topFileByDist, topDistVal, None)
  else:
    topFileByCorr, topCorrVal = c.correlationTop(target_crop, bucket)
    parent = topFileByDist
    if parent != topFileByCorr: parent = None
    return (parent, topDistVal, topCorrVal)
