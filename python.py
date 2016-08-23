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

# 일부 정거장 구하기
busstops = generate_busstops(sampling_mbus)
data = {'busstops': busstops, 'busroutes': ''}
generate_template_html(data, 'all_busstop.html')


# 버스 정보 읽기와 필터링
import pandas as pd

bus_df = pd.read_csv('bus.tsv', names=["busRouteNm", "busRouteId", "stationNo", "stationNm", "x", "y"], sep='\t')

mbus_df = bus_df[bus_df['stationNo']!='0']
mbus_df = mbus_df[mbus_df['stationNo']!='미정차']
mbus_df = mbus_df[mbus_df['stationNo']!='35331']

N_BUSSTOPS = 15

stops = mbus_df['stationNo'].value_counts()
d = stops[stops > N_BUSSTOPS].index.values.tolist()
mbus_df = mbus_df[mbus_df['stationNo'].isin(d)]
busstop_df = mbus_df.drop_duplicates(subset='stationNo', take_last=True)
# busstop_df

# 필터링 한 버스 정거장 map으로 출력
busstops = generate_busstops(busstop_df)
busroutes = ''
i = 0
for idx, row in busstop_df.iterrows():
    route = bus_df[bus_df['busRouteId']==row['busRouteId']]
    try:
        busroutes += generate_polyline("poly"+str(i), route, i)
    except TypeError:
        print ("cannot concatenate 'str' and 'NoneType' objects")
    i += 1
    
data = {'busstops': busstops, 'busroutes': busroutes}
generate_template_html(data)


# 24138 버스 정거장에 다니는 버스
#127.097975007	37.512839385
#     버스 정거장에 다니는 버스
#     각 버스의 노선

# 1 버스 정거장에 다니는 버스

import pandas as pd

bus_df = pd.read_csv('bus.tsv', names=["busRouteNm", "busRouteId", "stationNo", "stationNm", "x", "y"], sep='\t')

mbus_df = bus_df[bus_df['stationNo']!='0']
mbus_df = mbus_df[mbus_df['stationNo']!='미정차']
mbus_df = mbus_df[mbus_df['stationNo']!='35331']

mbus_df = mbus_df[mbus_df['stationNo']=='24138']
station_df = mbus_df.drop_duplicates(subset='busRouteId', take_last=True)

#2 각 버스의 노선

busstops = generate_busstops(station_df.drop_duplicates(subset='stationNo', take_last=True))
busroutes = ''
i = 0
for idx, row in station_df.iterrows():
    route = bus_df[bus_df['busRouteId']==row['busRouteId']]
#     print(route)
    busroutes += generate_polyline('poly'+str(i), route, i)
    i += 1
    
data = {'busstops': busstops, 'busroutes': busroutes}
generate_template_html(data, 'busstop_specific.html')
# 버스가 많은 정차하는 버스 정거장을 클러스러링한다.

#     버스 정거장 선택
#     시각화
#     클러스터링
#     클러스터링 후 시각화

#1 버스 정거장 선택

import pandas as pd
import re

bus_df = pd.read_csv('bus.tsv', names=["busRouteNm", "busRouteId", "stationNo", "stationNm", "x", "y"], sep='\t')

mbus_df = bus_df[bus_df['stationNo']!='0']
mbus_df = mbus_df[mbus_df['stationNo']!='미정차']
#차고지 빼기
#mbus_df = mbus_df[ mbus_df['stationNm']] 
#for sta_no in stations:
    #mbus_df = mbus_df[ mbus_df['stationNm']]


N_BUSSTOPS = 10

stops = mbus_df['stationNo'].value_counts()
d = stops[stops > N_BUSSTOPS].index.values.tolist()
mbus_df = mbus_df[mbus_df['stationNo'].isin(d)]
busstop_df = mbus_df.drop_duplicates(subset='stationNo', take_last=True)
# busstop_df


#2 시각화

busstops = generate_busstops(busstop_df)
busroutes = ''
# i = 0
# for idx, row in busstop_df.iterrows():
#     route = bus_df[bus_df['busno']==row['busno']]
#     busroutes += generate_polyline('poly' + str(i), route, i)
#     i += 1
    
data = {'busstops': busstops, 'busroutes': busroutes}
generate_template_html(data, 'busstop_origin.html')

#3 클러스터링

from sklearn.cluster import KMeans
from sklearn import metrics

print(busstop_df.head())
X = busstop_df[['x', 'y']]
y = busstop_df['busRouteId']
cluster_range = range(2, 15)
vmeasures = []

for n_cluster in cluster_range:

    # km = KMeans(n_clusters=7, init='random', max_iter=100, n_init=1, verbose=1)
    km = KMeans(init='k-means++', n_clusters=n_cluster, n_init=10)

#     print "Clustering sparse data with %s" % km
    km.fit(X)
#     print '----------------------------------------------------'
#     print n_cluster
#     print "Homogeneity: %0.3f" % metrics.homogeneity_score(y, km.labels_)
#     print "Completeness: %0.3f" % metrics.completeness_score(y, km.labels_)
#     print "V-measure: %0.3f" % metrics.v_measure_score(y, km.labels_)
#     print "Adjusted Rand-Index: %.3f" % metrics.adjusted_rand_score(y, km.labels_)
#     vmeasures.append(metrics.v_measure_score(y, km.labels_))
    vmeasures.append(metrics.silhouette_score(X, km.labels_, metric='euclidean'))
    
import matplotlib.pyplot as plt
plt.plot(cluster_range, vmeasures)
    
plt.xlabel('# cluster')
plt.ylabel('v measure')
plt.autoscale(tight=True)
plt.grid()
plt.show()


#4 클러스터링 후 시각화
best_clusters = 9
km = KMeans(init='k-means++', n_clusters=best_clusters, n_init=10)
km.fit(X)
# print km.cluster_centers_
centers = pd.DataFrame(km.cluster_centers_, columns=['x', 'y'])

busstops = generate_busstops(centers)
busroutes = ''
# i = 0
# for idx, row in busstop_df.iterrows():
#     route = bus_df[bus_df['busno']==row['busno']]
#     busroutes += generate_polyline('poly' + str(i), route, i)
#     i += 1
    
data = {'busstops': busstops, 'busroutes': busroutes}
generate_template_html(data, 'busstop_cluster_centers.html')

# DBSCAN로 이상치인 홀로 떨어진 빈도수 높은 버스 정거장 찾기

#     DBSCAN로 이상치 찾기
#     시각화

#1. DBSCAN로 이상치 찾기
from collections import namedtuple

from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer
from sklearn.cluster import DBSCAN

X['sx'] = X.x
X['sy'] = X.y

ss = StandardScaler()
X['sx'] = ss.fit_transform(X.sx)
X['sy'] = ss.fit_transform(X.sy)
# print(X)

Param = namedtuple('Param', ['eps', 'min_samples'])
params = [Param(0.45, 2), Param(0.30, 2), Param(0.35, 2), Param(0.40, 2), 
            Param(0.45, 4), Param(0.30, 4), Param(0.35, 4), Param(0.40, 4), 
            Param(0.45, 3), Param(0.30, 3), Param(0.35, 3), Param(0.40, 3)]
# print(X.values)
for param in params:
    dbscan = DBSCAN(eps=param.eps, min_samples=param.min_samples).fit(X[['sx', 'sy']].values)
    labels = dbscan.labels_
    outliers = X[labels == -1]
    
    print(param)
#     print(labels)
    print(outliers)
#     print("V-measure: %0.3f" % metrics.v_measure_score(y, labels))
    print(metrics.silhouette_score(X, labels, metric='euclidean'))

# busstops = generate_busstops(outliers)
# busroutes = ''
    
# data = {'busstops': busstops, 'busroutes': busroutes}
# generate_template_html(data, 'busstop_cluster_outlier.html')

#2 시각화
best_param = Param(eps=0.3, min_samples=3)
dbscan = DBSCAN(eps=best_param.eps, min_samples=best_param.min_samples).fit(X[['sx', 'sy']].values)
labels = dbscan.labels_
outliers = X[labels == -1]

busstops = generate_busstops(outliers)
busroutes = ''
    
data = {'busstops': busstops, 'busroutes': busroutes}
generate_template_html(data, 'busstop_cluster_outlier.html')