#-*- coding: utf-8 -*-
import urllib2, urllib 
import json 
import unicodecsv as csv
from socket import timeout
import logging 
import pandas

parameters = {} 
parameters['strSrch'] ='';

target = 'http://m.bus.go.kr/mBus/bus/getBusRouteList.bms'
parameters = urllib.urlencode(parameters) 
proxy_handler = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener) 
try:
    handler = urllib2.urlopen(urllib2.Request(target, parameters))
except urllib2.URLError :
    print ("urllib2.URLError: <urlopen error [Errno 60] Operation timed out>")
try:
    f = handler.read()
except TypeError: 
    print ("object is not callable")
handler.close()
j = json.loads(f.decode('cp949')) 
buses = j["resultList"]

for bus in buses:
    parameters = {} 
    parameters['busRouteId'] = bus['busRouteId']

    target = 'http://m.bus.go.kr/mBus/bus/getRouteAndPos.bms'
    parameters = urllib.urlencode(parameters)
    proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener) 
    try:
        handler = urllib2.urlopen(urllib2.Request(target, parameters))
    except urllib2.URLError :
        print ("urllib2.URLError: <urlopen error [Errno 60] Operation timed out>")
    try:
        f = handler.read()
    except TypeError: 
        print ("object is not callable")
    handler.close()
    j = json.loads(f.decode('cp949')) 
    try:
        routes = j["resultList"]
    except:
        print ("KeyError: 'resultList'")
    csvfile = open('./bus.tsv', 'a')
    writer = csv.writer(csvfile, delimiter=',')
    for route in routes:
        if ((route['stationNm'] == "미정차") or (route['stationNm'] == "0" )):
            continue
        busRouteNm = route['busRouteNm'] 
        busRouteId = route['busRouteId'] 
        stationNm = route['stationNm'] 
        stationNo = route['stationNo'] 
        x = route['gpsX'] 
        y = route['gpsY'] 
        try:
            l = '\t'.join([busRouteNm, busRouteId, stationNo, stationNm, x, y])
        except TypeError:
            print ("TypeError: sequence item 2: expected string or Unicode, NoneType found")      
        writer.writerow([l])