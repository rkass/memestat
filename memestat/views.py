from django.shortcuts import render_to_response
from django.template import RequestContext
from stats.models import *

def orderMemes(macroGroup):
  ret = Meme.objects.filter(classification = macroGroup[0])
  for mac in macroGroup:
    ret |= Meme.objects.filter(classification = mac)
  return ret.order_by('topDist')

def home(request):
  topMeme = TopMacro.objects.latest('id')
  sinkingStone = SinkingStone.objects.latest('id')
  shootingStar = ShootingStar.objects.latest('id')
  topMemeImg = orderMemes(topMeme.macros.all())[0].fullSizeLink
  sinkingStoneImg = orderMemes(sinkingStone.macros.all())[0].fullSizeLink
  shootingStarImg = orderMemes(shootingStar.macros.all())[0].fullSizeLink
  return render_to_response('home.html', {
                                          'sinkingStone' : sinkingStone.macros.all()[0].name,
                                          'shootingStar' : shootingStar.macros.all()[0].name,
                                          'topMeme' : topMeme.macros.all()[0].name,
                                          'topMemeImg' : topMemeImg, 
                                          'shootingStarImg' : shootingStarImg,
                                          'sinkingStoneImg' : sinkingStoneImg,
                                          'topMemeUvt' : topMeme.dailyScore,
                                          'topMemeDc' : topMeme.dailyChange,
                                          'shootingStarUvt' : shootingStar.dailyScore,
                                          'shootingStarDc' : shootingStar.dailyChange,
                                          'sinkingStoneUvt' : sinkingStone.dailyScore,
                                          'sinkingStoneDc' : sinkingStone.dailyChange}, context_instance=RequestContext(request))
