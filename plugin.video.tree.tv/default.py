#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib2
import urllib
import json
import xbmcgui
import xbmcplugin
import xbmcaddon
import re,base64,random,time,cookielib

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from urllib import unquote, quote, quote_plus
Addon = xbmcaddon.Addon( id = 'plugin.video.tree.tv' )
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


def GET(target, post=None):
    #print target
    #print post
    #http://tree.tv/users/index/auth?mail=booze%40coil.io&pass=666131313&social=0
    if post==1:
        cookiejar = cookielib.CookieJar()
        urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        request = urllib2.Request("http://tree.tv/users/index/auth?mail=booze%40coil.io&pass=666131313&social=0")
        url = urlOpener.open(request)
        urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
        request = urllib2.Request(target)
        url = urlOpener.open(request)
        red = url.read()
        return red
    try:
        req = urllib2.Request(url = target, data = post)
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
        req.add_header('Accept', '*/*')
        req.add_header('Accept-Language', 'ru-RU')
        resp = urllib2.urlopen(req)
        CE = resp.headers.get('content-encoding')
        http = resp.read()
        resp.close()
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
    listitem=xbmcgui.ListItem('Поиск',iconImage = addon_icon, thumbnailImage = addon_icon)
    uri = construct_request({
        'func': 'serch'
        })
    xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
    search('!zzxd@34')
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)

def serch(params):
    params={}
    kbd = xbmc.Keyboard()
    kbd.setDefault('')
    kbd.setHeading('Поиск')
    kbd.doModal()
    out=''
    if kbd.isConfirmed():
        out = kbd.getText()
    params['usersearch']=out
    #print params
    search(params)
    
def search(params):
    shw=1
    try: 
        http=GET(params['url'])
        shw=0
    except:
        try: 
            http=GET('http://tree.tv/search/index','usersearch='+params['usersearch'])
            shw=0
        except: 
            http=GET('http://tree.tv/search/index')
            
    
    m=BeautifulSoup(http)
    
    cats=m.find('div',attrs={'class':'scroll-pane'})
    if cats and shw==1: 
        ll=cats.findAll('a')
        for l in ll:

            listitem=xbmcgui.ListItem(l.string,iconImage = addon_icon, thumbnailImage = addon_icon)
            uri = construct_request({'func': 'search','url':'http://tree.tv/default/index?sortType=new&type=big_list&janrs='+l['rel'],'img':addon_icon,'title':l.string})
            xbmcplugin.addDirectoryItem(hos, uri, listitem, True)

    z=m.findAll('div',attrs={"class":"item"})
    for n in z:
        #print n.prettify()
        if n.find('a'):

            
            tz= n.find('h2').find('a')
            ttl=tz.string.encode('utf-8')
            lnk=tz['href'].encode('utf-8')
            tz=n.find(src=re.compile('/public/.*'))
            #print ttl
            #print lnk
            if tz: 
                img='http://tree.tv'+tz['src']
            else: img=addon_icon

            listitem=xbmcgui.ListItem(ttl,iconImage = img, thumbnailImage = img)
            uri = construct_request({'func': 'getvid','url':lnk,'img':addon_icon,'title':ttl})
            xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
           
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
def getcat (params):
    
    rel=params['url']
    page=1
    while (page<10):
        host="http://tree.tv/default/index/list/?type=list&sortType=prosmotr&sortYear=2013&janrs%5B%5D="+rel+"&page=%s"%page
        #print host
        http = GET(host)
        json1=json.loads(http)
        for movie in json1:
            title= movie['name'].encode('utf-8')
            img="http://tree.tv/"+movie['src'].encode('utf-8')
            href=movie['name_for_url'].encode('utf-8')
            listitem=xbmcgui.ListItem(title,iconImage = img, thumbnailImage = img)
            try:
                uri = construct_request({'func': 'getvid','url':href,'img':img,'title':title})
            except:
                uri = construct_request({'func': 'getvid','url':href,'img':img,'title':'fail'})
            xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
        page=page+1
    '''content = beautifulSoup.find('div', attrs={'id':'dle-content'})
    nxt= content.findAll('a')[-1]
    for n in str(content).split('<div class="prew-film-title">'):
        m=BeautifulSoup(n)
        link= m.find('div',attrs={'class':'box4'})
        try:
            title= link.find('img')['alt'].encode('utf-8')
            img= link.find('img')['src'].encode('utf-8')
            if 'www.kino-ray.com' not in img: img='http://www.kino-ray.com%s'%img
            href=link.find('a')['href']
            listitem=xbmcgui.ListItem(title,iconImage = img, thumbnailImage = img)
            uri = construct_request({
                'func': 'getvid',
                'url':href,
                'img':img,
                'title':title
                })
            xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
        except: pass
    if 'Далее' in str(nxt):
        listitem=xbmcgui.ListItem('Далее',iconImage = addon_icon, thumbnailImage = addon_icon)
        uri = construct_request({
            'func': 'getcat',
            'url':nxt['href']
            })
        xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
    xbmcplugin.setContent(hos, 'movies')'''
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
    
def getvid(params):
    host="http://tree.tv/"+params['url']
    img=params['img']
    title=params['title']
    http = GET(host,1)
    beautifulSoup = BeautifulSoup(http)

    multi=beautifulSoup.findAll('div',attrs={'class':'film_actions'})

    for list in multi:

        href= list.find('a', attrs={'class':'download_mini noukraine'})['href']
        listitem=xbmcgui.ListItem(href.split('/')[-1],iconImage = addon_icon, thumbnailImage = params['img'])
        uri = construct_request({
            'func': 'get_movie',
            'href':href
            })
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(hos, uri, listitem)
    xbmcplugin.addSortMethod(hos, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
from urllib import unquote, quote, quote_plus
    
    
def get_movies(params):
    http=GET(params['url'])
    #print params['url']
    beautifulSoup = BeautifulSoup(http)
    txt=str(beautifulSoup).replace(' онлайн в хорошем качестве HD 720p','').replace(' онлайн в хорошем качестве','').replace('<font>Смотреть фильм ','').replace('<font>Смотреть сериал ','').replace('Смотреть онлайн фильм в хорошем качестве HD 720p','').replace('<font><font>','<font>').replace('<font></font>','').replace('<font> </font>','').replace('</font></font>','</font>')
    m=re.findall('<font>(?!.*Смотреть)(.+?)</font><br /><br /><iframe src="(.+?)"',txt)

    if not m: m= re.findall('</font>(.+?)</font><br /><br /><iframe src="(.+?)"',txt)
    if not m: m= re.findall('</font>(.+?)</font></i><br /><br /><iframe src="(.+?)"',txt)

    for n in m: 
        #print n
        listitem=xbmcgui.ListItem(n[0].replace('смотреть онлайн',''),iconImage = addon_icon, thumbnailImage = params['img'])
        uri = construct_request({
            'func': 'get_movie',
            'url':n[1].replace('amp;','')
            })
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(hos, uri, listitem)
    if not m: 

        m= re.findall('iframe src="(.+?)"',str(beautifulSoup))
        for n in m:
            listitem=xbmcgui.ListItem(params['title'].replace('смотреть онлайн',''),iconImage = addon_icon, thumbnailImage = params['img'])
            uri = construct_request({
                'func': 'get_movie',
                'url':n.replace('amp;','')
                })
            listitem.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(hos, uri, listitem)
        
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
def get_movie(params):
    #print params['href']
    item = xbmcgui.ListItem(path=params['href'])
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

            
    
def getinfo(param):
    info={}
    for infostring in param:
        try:
            m=re.search('[^<>]+<',str(infostring))
            comm = str( m.group(0)[:-1])
            m=re.search('[^<>]+</a',str(infostring))
            data = str( m.group(0)[:-3])
            #print "%s:%s"%(comm,data)
            if comm=="Год: ": info['year']=int(data)
            if comm=="Жанр: ": info['genre']=data
            if comm=="Режиссер: ": info['director']=data
            if comm=="Автор оригинала: ": info['writer']=data
        except: pass
    #print info
    return info

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

