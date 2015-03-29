#!/usr/bin/python
# -*- coding: utf-8 -*-
#/*
# *      Copyright (C) 2011 Silen
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# */

import urllib2
import urllib
import simplejson as json
import xbmcgui
import xbmcplugin
import xbmcaddon
import re,base64,random,time

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from urllib import unquote, quote, quote_plus
Addon = xbmcaddon.Addon( id = 'plugin.video.truba.com' )
__language__ = Addon.getLocalizedString

addon_icon    = Addon.getAddonInfo('icon')
addon_fanart  = Addon.getAddonInfo('fanart')
addon_path    = Addon.getAddonInfo('path')
addon_type    = Addon.getAddonInfo('type')
addon_id      = Addon.getAddonInfo('id')
addon_author  = Addon.getAddonInfo('author')
addon_name    = Addon.getAddonInfo('name')
addon_version = Addon.getAddonInfo('version')

import Cookie, cookielib
hos = int(sys.argv[1])
headers  = {
	'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)',
	'Accept'     :' text/html, application/xml, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*',
	'Accept-Language':'ru-RU,ru;q=0.9,en;q=0.8',
	'Accept-Charset' :'utf-8, utf-16, *;q=0.1',
	'Accept-Encoding':'identity, *;q=0'}
	
cook_file = xbmc.translatePath('special://temp/'+ 'truba.cookies')

def GET(target, post=None):
	target=target.replace('//page','/page')
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
			
def doSearch(params):
	kbd = xbmc.Keyboard()
	kbd.setDefault('')
	kbd.setHeading("Поиск")
	kbd.doModal()
	out=''
	if kbd.isConfirmed():
		out = kbd.getText().decode('koi8-r')
		#print out
	#http://truba.com/search.php?q=%CD%C1%CD%C1&c=0
	url='http://truba.com/search.php?q=%s&c=0'%str(out)
	url=url
	print url
	par={}
	par['mpath']=url
	playfolder(par)

def run_settings(params):
    Addon.openSettings()
	
def cats(params):
	http = GET('http://truba.com/')
	#print http
	if http == None: return False
	beautifulSoup = BeautifulSoup(http)
	navigator = beautifulSoup.find('li', attrs={'class': 'navigator'})
	cat=navigator.findAll('li')
	regex=re.compile('<a href="(.+)".+title="(.+)"')
	data= regex.findall(str(navigator))
	for g in data: 
		#print g[1]
		try:
			li = xbmcgui.ListItem(g[1], iconImage = addon_icon, thumbnailImage = addon_icon)
			uri = construct_request({
				'func': 'playfolder',
				'mpath': 'http://truba.com/'+g[0]
			})
			li.setProperty('fanart_image', addon_fanart)
			xbmcplugin.addDirectoryItem(hos, uri, li, True)
		except: pass
	xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)

def tags(params):
	http = GET(params['mpath'])
	#print http
	if http == None: return False
	beautifulSoup = BeautifulSoup(http)
	navigator = beautifulSoup.find('li', attrs={'id': 'tags'})
	cat=navigator.findAll('li')
	regex=re.compile('<a href="(.+)".+title="(.+)">(.+)</a>')
	data= regex.findall(str(navigator))
	
	for g in data: 
		print g
		try:
			li = xbmcgui.ListItem(g[2], iconImage = addon_icon, thumbnailImage = addon_icon)
			uri = construct_request({
				'func': 'playfolder',
				'mpath': 'http://truba.com/'+g[0]
			})
			li.setProperty('fanart_image', addon_fanart)
			xbmcplugin.addDirectoryItem(hos, uri, li, True)
		except: pass
	xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
	
def mainScreen(params):

	li = xbmcgui.ListItem('Поиск', iconImage = addon_icon, thumbnailImage = addon_icon)
	uri = construct_request({
		'func': 'doSearch'
	})
	li.setProperty('fanart_image', addon_fanart)
	#xbmcplugin.addDirectoryItem(hos, uri, li, True)

	http = GET('http://truba.com/')
	#print http
	if http == None: return False

	li = xbmcgui.ListItem('Тэги', iconImage = addon_icon, thumbnailImage = addon_icon)
	uri = construct_request({
		'func': 'tags',
		'mpath':'http://truba.com/'
	})
	li.setProperty('fanart_image', addon_fanart)
	xbmcplugin.addDirectoryItem(hos, uri, li, True)
	
	li = xbmcgui.ListItem('Категории', iconImage = addon_icon, thumbnailImage = addon_icon)
	uri = construct_request({
		'func': 'cats'
	})
	li.setProperty('fanart_image', addon_fanart)
	xbmcplugin.addDirectoryItem(hos, uri, li, True)
		
	beautifulSoup = BeautifulSoup(http)
	navigator = beautifulSoup.find('li', attrs={'class': 'navigator'})

	regex=re.compile('<p class="name" title="(.+) &mdash.+[\s+].+href="(.+)".+src="(.+)" alt=')
	data= regex.findall(str(http))
	for g in data: 
		try:
			regex=re.compile('\d+')
			num= regex.findall(g[1])[0]
			li = xbmcgui.ListItem(g[0].decode('koi8-r'), iconImage = addon_icon, thumbnailImage = g[2])
			uri = construct_request({
				'func': 'play',
				'mpath': g[1]
			})
			li.setProperty('IsPlayable', 'true')
			li.setProperty('fanart_image', addon_fanart)
			xbmcplugin.addDirectoryItem(hos, uri, li, False)
		except: pass

	xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
	
def playfolder(params):

	url= params['mpath']
	http = GET(url)
	regex=re.compile('<p class="name" title="(.+) &mdash.+[\s+].+href="(.+)".+src="(.+)" alt=')
	data= regex.findall(str(http))
	for g in data: 
		try:
			regex=re.compile('\d+')
			num= regex.findall(g[1])[0]
			li = xbmcgui.ListItem(g[0].decode('koi8-r'), iconImage = addon_icon, thumbnailImage = g[2])
			uri = construct_request({
				'func': 'play',
				'mpath': g[1]
			})
			li.setProperty('IsPlayable', 'true')
			li.setProperty('fanart_image', addon_fanart)
			xbmcplugin.addDirectoryItem(hos, uri, li, False)
		except: pass
	beautifulSoup = BeautifulSoup(http)
	paginator = beautifulSoup.find('div', attrs={'class': 'paginator'})
	if paginator:
		pages=paginator.findAll('a')
		for g in pages: 
			link= g['href']
			title= g.string
			if title:
				title="Перейти на страницу %s"% title.encode('utf-8')
				li = xbmcgui.ListItem(title, iconImage = addon_icon, thumbnailImage = addon_icon)
				uri = construct_request({
					'func': 'playfolder',
					'mpath': link
				})
				li.setProperty('fanart_image', addon_fanart)
				xbmcplugin.addDirectoryItem(hos, uri, li, True)
	xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
def play(params):
	url= params['mpath']
	http = GET(url)
	#<meta content="http://truba.com/video/0356/355421.mp4" property="og:video">
	regex=re.compile('http://truba.com/video/[0-9]+/[0-9]+.mp4')
	link= regex.findall(http)[0]
	print link
	item = xbmcgui.ListItem(path=link)
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
	mainScreen(params)
if func != None:
	try: pfunc = globals()[func]
	except:
		pfunc = None
		xbmc.log( '[%s]: Function "%s" not found' % (addon_id, func), 4 )
		showMessage('Internal addon error', 'Function "%s" not found' % func, 2000)
	if pfunc: pfunc(params)

