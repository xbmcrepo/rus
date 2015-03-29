#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib2
import urllib
import simplejson as json
import xbmcgui
import xbmcplugin
import xbmcaddon
import re,base64,random,time

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from urllib import unquote, quote, quote_plus
Addon = xbmcaddon.Addon( id = 'plugin.video.goha.tv' )
__language__ = Addon.getLocalizedString

addon_icon    = Addon.getAddonInfo('icon')
addon_fanart  = Addon.getAddonInfo('fanart')
addon_path    = Addon.getAddonInfo('path')
addon_type    = Addon.getAddonInfo('type')
addon_id      = Addon.getAddonInfo('id')
addon_author  = Addon.getAddonInfo('author')
addon_name    = Addon.getAddonInfo('name')
addon_version = Addon.getAddonInfo('version')

VERSION = '4.3as'
DOMAIN = '131896016'
GATrack='UA-30985824-2'
try:
    import platform
    xbmcver=xbmc.getInfoLabel( "System.BuildVersion" ).replace(' ','_').replace(':','_')
    UA = 'XBMC/%s (%s; U; %s %s %s %s) %s/%s XBMC/%s'% (xbmcver,platform.system(),platform.system(),platform.release(), platform.version(), platform.machine(),addon_id,addon_version,xbmcver)
except:
    UA = 'XBMC/Unknown %s/%s/%s' % (urllib.quote_plus(addon_author), addon_version, urllib.quote_plus(addon_name))
hos = int(sys.argv[1])
headers  = {
	'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
	'Accept'     :' text/html, application/xml, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*',
	'Accept-Language':'ru-RU,ru;q=0.9,en;q=0.8',
	'Accept-Charset' :'utf-8, utf-16, *;q=0.1',
	'Accept-Encoding':'identity, *;q=0'
}
httpHeaderUserAgent='Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)'
try:
    from hashlib import md5
except:
    from md5 import md5
	
if not Addon.getSetting('GAcookie'):
    from random import randint
    GAcookie ="__utma%3D"+DOMAIN+"."+str(random.randint(0, 0x7fffffff))+"."+str(random.randint(0, 0x7fffffff))+"."+str(int(time.time()))+"."+str(int(time.time()))+".1%3B"
    Addon.setSetting('GAcookie', GAcookie)
if not Addon.getSetting('uniq_id'):
    from random import randint
    uniq_id=random.random()*time.time()
    Addon.setSetting('uniq_id', str(uniq_id))

def get_random_number():
    return str(random.randint(0, 0x7fffffff))

import Cookie, cookielib

cook_file = xbmc.translatePath('special://temp/'+ 'anidub.cookies')

def GET(target, post=None):
	print target
	try:
			cookiejar = cookielib.MozillaCookieJar()
			urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
			request = urllib2.Request(url = target, data = post, headers = headers)
			url = urlOpener.open(request)
			http=url.read()
			return http
	except Exception, e:
			xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
			showMessage('HTTP ERROR', e, 5000)

def construct_request(params):
	return '%s?%s' % (sys.argv[0], urllib.urlencode(params))
	
def showMessage(heading, message, times = 3000, pics = addon_icon):
	try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading.encode('utf-8'), message.encode('utf-8'), times, pics.encode('utf-8')))
	except Exception, e:
		xbmc.log( '[%s]: showMessage: Transcoding UTF-8 failed [%s]' % (addon_id, e), 2 )
		try: xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")' % (heading, message, times, pics))
		except Exception, e:
			xbmc.log( '[%s]: showMessage: exec failed [%s]' % (addon_id, e), 3 )

def run_settings(params):
    Addon.openSettings()

def mainMain(params):
	http = GET('http://gohatv.testsite.goha.ru/app/tv/data.php/stream/active/ru.js')
	data=http.replace("if (window.gohaTV) gohaTV.callback('stream/active/ru.js', ",'').replace('\n','')
	data=data[:-1]
	#print data
	json1=json.loads(data)
	streams= json1['streams']
	for shows in streams:
		print shows['stream']
		title='[COLOR FFFF0000]%s[/COLOR] [COLOR FF00FF00]%s[/COLOR]: %s'%(shows['stream']['provider'].encode('utf-8'),shows['user']['name'].encode('utf-8'),(shows['user']['desc'].encode('utf-8')))
		listitem=xbmcgui.ListItem(str(title).replace('\n',''),iconImage = addon_icon, thumbnailImage = addon_icon)
		#plugin://plugin.video.engineeredchaos.own3Dtv/?mode=2&streamID=42146&name=Athene&videoType=1
		uri = construct_request({
			'func': shows['stream']['provider'].replace('.',''),
			'name': shows['stream']['id']
			})
		#if shows['stream']['provider']=='own3d.tv':
		#	uri='plugin://plugin.video.engineeredchaos.own3Dtv/?mode=2&streamID=%s&name=%s&videoType=1'%(str(shows['stream']['id'].encode('utf-8')),urllib.quote_plus(str((shows['user']['desc'].encode('utf-8'))).replace('\n','')))
		#	print uri
		listitem.setProperty('IsPlayable', 'true')
		xbmcplugin.addDirectoryItem(hos, uri, listitem)
	beautifulSoup = BeautifulSoup(http)
	content = beautifulSoup.findAll('div', attrs={'class':'footer'})
	#streams = content.findAll('a', attrs={'class':'stream-item'})
	#for t in streams: print t
	#print content
	xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
from urllib import unquote, quote, quote_plus

def cybergametv(params):
	print params
	http=GET('http://api.cybergame.tv/p/embed.php?c=%s&w=650&h=365&type=embed'%params['name'])
	beautifulSoup = BeautifulSoup(http)
	print http
	link='http://api.cybergame.tv/p/playlist.smil?channel=%s'%params['name']
	ht=GET(link)
	
	lnk= BeautifulSoup(ht).findAll('meta')[0]['base']
	asd=re.findall('http://.+.m3u8',str(http))
	print asd
	if not asd: asd=lnk
	else: ads=asd[0]
	try:
		item = xbmcgui.ListItem(path=asd)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
	except: pass
#play Justin
def justintv(params, play=False):
		name=params['name']
		name=name.replace('live_user_','')
		headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
			'Referer' : 'http://www.justin.tv/'+name}
		url1 = 'http://usher.justin.tv/find/'+name+'.json?type=live'
		#print url1
		data = json.loads(GET(url1))
		#print url1
		#print data
		if data == []:
			showMessage('Twitch.TV','Стрим не найден')
			return
		else:
			try:
				token = ' jtv='+data[0]['token'].replace('\\','\\5c').replace(' ','\\20').replace('"','\\22')
			except:
				showMessage('Twitch.TV','Стрим не найден')
				return
			rtmp = data[0]['connect']+'/'+data[0]['play']
			swf = ' swfUrl=%s swfVfy=1' % getSwfUrl(name)
			Pageurl = ' Pageurl=http://www.justin.tv/'+name
			url1 = rtmp+token+swf+Pageurl
			#print url1
			if play == True:
				info = xbmcgui.ListItem(name)
				playlist = xbmc.PlayList(1)
				playlist.clear()
				playlist.add(url1, info)
				xbmc.executebuiltin('playlist.playoffset(video,0)')
			else:
				item = xbmcgui.ListItem(path=url1)
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
def getSwfUrl(channel_name):
        """Helper method to grab the swf url, resolving HTTP 301/302 along the way"""
        base_url = 'http://www.justin.tv/widgets/live_embed_player.swf?channel=%s' % channel_name
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                   'Referer' : 'http://www.justin.tv/'+channel_name}
        req = urllib2.Request(base_url, None, headers)
        response = urllib2.urlopen(req)
        return response.geturl()

def newlivestreamcom(params):
	link='http://new.livestream.com//assets/plugins/html5.js?%s'%params['name']
	print link
	http=GET(link)
	print http
	url='http://livestream-f.akamaihd.net/43923_1673924_9d6fcd03_1_2320@74372?v=2.10.3&fp=WIN%2011,5,31,135&r=YDQQH&g=OLPLTEVMGCNJ'	
	item = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
def get_params(paramstring):
	param=[]
	if len(paramstring)>=2:
		params=paramstring
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	if len(param) > 0:
		for cur in param:
			param[cur] = urllib.unquote_plus(param[cur])
	return param

params = get_params(sys.argv[2])
try:
	func = params['func']
	del params['func']
except:
	func = None
	xbmc.log( '[%s]: Primary input' % addon_id, 1 )
	mainMain(params)
if func != None:
	try: pfunc = globals()[func]
	except:
		pfunc = None
		xbmc.log( '[%s]: Function "%s" not found' % (addon_id, func), 4 )
		showMessage('Internal addon error', 'Function "%s" not found' % func, 2000)
	if pfunc: pfunc(params)

