#-*- coding: utf-8 -*-
# google map 파일 출력
from string import Template

colors = ["FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF", "000000",
        "800000", "008000", "000080", "808000", "800080", "008080", "808080",
        "C00000", "00C000", "0000C0", "C0C000", "C000C0", "00C0C0", "C0C0C0",
        "400000", "004000", "000040", "404000", "400040", "004040", "404040",
        "200000", "002000", "000020", "202000", "200020", "002020", "202020",
        "600000", "006000", "000060", "606000", "600060", "006060", "606060",
        "A00000", "00A000", "0000A0", "A0A000", "A000A0", "00A0A0", "A0A0A0",
        "E00000", "00E000", "0000E0", "E0E000", "E000E0", "00E0E0", "E0E0E0"]

def generate_busstops(df):
    coos = ',\n'.join(['new google.maps.LatLng(%s, %s)' %(r['y'] ,r['x']) for i, r in df.iterrows()])
    return 'var busstops = [{0}];'.format(coos)

def generate_chargers(df):
    coos = ',\n'.join(['new google.maps.LatLng(%s, %s)' %(r['y'] ,r['x']) for i, r in df.iterrows()])
    return 'var chargers = [{0}];'.format(coos)

def generate_polyline(valname, df, idx):
    coos = ',\n'.join(['new google.maps.LatLng(%s, %s)' %(r['y'] ,r['x']) for i, r in df.iterrows()])
    valcoos =  'var {0} = [{1}];'.format(valname, coos)

    polyline_template = """
                        {0}
                        var {1}_ = new google.maps.Polyline({{
                        path: {1},
                        strokeColor: "#{2}",
                        strokeOpacity: 0.8,
                        strokeWeight: 3
                        }});
                        {1}_.setMap(map);"""
    try :       
        return polyline_template.format(valcoos, valname, colors[idx])
    except IndexError :
        print ("list index out of range")

# data = {'busstops': busstops, 'busroutes':busroutes}
def generate_template_html(data, outfilename='busmap.html'):
    infile = open('map_temp.html')
    template = Template(infile.read())
    map_html = template.substitute(data)
    outfile = open(outfilename, 'w')
    outfile.write(map_html)

# 일부 버스 정보 샘플링 => map에 표시하기 위해
import pandas as pd
import numpy as np

bus_df = pd.read_csv('bus.tsv', names=["busRouteNm", "busRouteId", "stationNo", "stationNm", "x", "y"],sep='\t')

mbus_df = bus_df[bus_df['stationNo']!='0']
mbus_df = mbus_df[mbus_df['stationNo']!='미정차']
mbus_df = mbus_df[mbus_df['stationNo']!='35331']
# mbus_df.shape
sampling_mbus = mbus_df.loc[np.random.permutation(mbus_df.index)[:200]]

charger_df = pd.read_csv('ev_pos.csv', names=["a", "b", "c", "d", "x", "y"], sep=',')
mcharger_df = charger_df["a"].value_counts()
mcharger_df = mcharger_df[mcharger_df["a"].isin(d)]
mcharger_df = mcharger_df.drop_duplicates(subset="a", take_last=True)

# 일부 정거장 구하기
busstops = generate_busstops(sampling_mbus)
chargers = generate_chargers(mcharger_df)
data = {'busstops': busstops, 'busroutes': '', 'chargers': chargers}
generate_template_html(data, 'all_busstop.html')

