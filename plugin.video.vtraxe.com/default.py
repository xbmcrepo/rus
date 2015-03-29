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
Addon = xbmcaddon.Addon( id = 'plugin.video.vtraxe.com' )
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
    try:
        req = urllib2.Request(url = target, data = post)
        req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
        #req.add_header('Host',	'online.stepashka.com')
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
def doSearch(params):
    kbd = xbmc.Keyboard()
    kbd.setDefault('')
    kbd.setHeading("Поиск")
    kbd.doModal()
    out=''
    if kbd.isConfirmed():
        try:
            out = trans.detranslify(kbd.getText())
            out=str(out.encode("utf-8"))
        except:
            out = str(kbd.getText())
    url='http://yandex.ru/sitesearch?text='+out+'&web=0&l100n=ru&frame=1&v=2.0&searchid=1891946&encoding=utf-8&topdoc=xdm_e%3Dhttp%253A%252F%252Fcinema-hd.ru%26xdm_c%3Ddefault4923%26xdm_p%3D1'
    #print url
    par={}
    par['url']=url
    GetSearch(par)
    

def run_settings(params):
    Addon.openSettings()

def mainMain(params):
    http = GET('http://vtraxe.com/')
    if http == None: return False
    beautifulSoup = BeautifulSoup(http)
    
    content = beautifulSoup.find('div',attrs={'class':'cat-menu'})
    content=content.findAll('li')
    for num in content:	
        title=num.find('a').string
        url=num.find('a')['href']
        listitem=xbmcgui.ListItem(title,iconImage = addon_icon, thumbnailImage = addon_icon)
        uri = construct_request({
            'func': 'mainScreen',
            'url':url
            })
        xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
    
def mainScreen(params):
    host='http://vtraxe.com'+params['url']
    try:
        page=(params['page'])
    except:
        page=1
    if page==1:
        http = GET(host)
    else: 
        print str(page)
        http = GET(host+'/page/'+str(page))
    #print http
    if http == None: return False
    
    beautifulSoup = BeautifulSoup(http)

    #<table width="100%" cellspacing="1" cellpadding="1" border="0" style="padding-bottom: 1px;">
    content = beautifulSoup.findAll('div', attrs={'class': 'shortstory'})
    for n in content: 

        url= n.find('a')['href']
        title= n.find('div').string
        pic= n.find('img')['src']
        if 'vtraxe.com' not in pic:
            pic='http://vtraxe.com/%s'%pic
        #title=title.replace(' смотреть онлайн в хорошем качестве HD 720p бесплатно','')
        listitem=xbmcgui.ListItem(title,iconImage = addon_icon, thumbnailImage = pic)
        uri = construct_request({
            'func': 'get_movies',
            'url':url,
            'title':title,
            'img':pic
            })
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(hos, uri, listitem)
    
    listitem=xbmcgui.ListItem('Next',iconImage = addon_icon, thumbnailImage = addon_icon)
    uri = construct_request({
                'func': 'mainScreen',
                'page':int(int(page)+1),
                'url':params['url']
                })
    xbmcplugin.addDirectoryItem(hos, uri, listitem, True)
    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)

from urllib import unquote, quote, quote_plus
    
    
def get_movies(params):
    print params['url']

    http=GET(params['url'])
    para={}
    print http
    #<iframe width="645" height="455"
    m=re.findall('<iframe width="..." height="..." src="(.+)" frameborder="0"',http)
    http=GET( m[0])
    #print http
    m=re.findall("video_alt_url3: '(.+)/', ",http)
    if not m:
        m=re.findall("video_alt_url4: '(.+?)/', ",http)
    link= m[0].split("'")[0]
    print link
    listitem=xbmcgui.ListItem(params['title'].replace('смотреть онлайн',''),iconImage = addon_icon, thumbnailImage = params['img'])
    uri = construct_request({
        'func': 'get_moviex',
        'url':link
        })
    para['url']=link
    get_moviex(para)

    xbmcplugin.endOfDirectory(handle=hos, succeeded=True, updateListing=False, cacheToDisc=True)
def get_movie(params):
    http=GET(params['url'])
    soup = BeautifulSoup(http, fromEncoding="windows-1251")
    av=0
    for rec in soup.findAll('param', {'name':'flashvars'}):
        #print rec
        for s in rec['value'].split('&'):
            if s.split('=',1)[0] == 'uid':
                uid = s.split('=',1)[1]
            if s.split('=',1)[0] == 'vtag':
                vtag = s.split('=',1)[1]
            if s.split('=',1)[0] == 'host':
                host = s.split('=',1)[1]
            if s.split('=',1)[0] == 'vid':
                vid = s.split('=',1)[1]
            if s.split('=',1)[0] == 'oid':
                oid = s.split('=',1)[1]
            if s.split('=',1)[0] == 'hd':
                hd = s.split('=',1)[1]
        host=host.replace('vk.me','vk.com')
        video = host+'u'+uid+'/videos/'+vtag+'.360.mp4'
        if int(hd)==3:
            video = host+'u'+uid+'/videos/'+vtag+'.720.mp4'
        if int(hd)==2:
            video = host+'u'+uid+'/videos/'+vtag+'.480.mp4'
        if int(hd)==1:
            video = host+'u'+uid+'/videos/'+vtag+'.360.mp4'
        #print video
        item = xbmcgui.ListItem(path=video)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def get_moviex(params):    
    item = xbmcgui.ListItem(path=params['url'])
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

