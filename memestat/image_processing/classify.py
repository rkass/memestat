import compute as c

def classify(target, bucket):
  target_crop = c.centerCut(target)
  topFileByDist, topDistVal, count = c.distanceTop(target_crop, bucket)
  if count < 100:
    if topDistVal < 20:
      return (topFileByDist, topDistVal, None)
    else:
      return (None, topDistVal, None)
  elif topDistVal < 40:
    return (topFileByDist, topDistVal, None)
  else:
    topFileByCorr, topCorrVal = c.correlationTop(target_crop, bucket)
    parent = topFileByDist
    if parent != topFileByCorr: parent = None
    return (parent, topDistVal, topCorrVal)
