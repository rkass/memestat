import urllib3
f = open('imagemacros/new.jpg', 'wb')
f.write(urllib3.PoolManager().request('GET', 'http://i.imgur.com/By9tPxf.jpg').data)
f.close()

