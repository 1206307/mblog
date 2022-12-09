from django.shortcuts import render
from django.http import HttpResponse,Http404
import requests
# Importing the libraries
import base64
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
# Importing the dataset 
from sklearn.cluster import KMeans
# Create your views here.

def kmeanshow(request,slug):
    bas64string = slug
    # pointsarray = np.array([0,0])
    # df=connectAUODB.getLcmODSBySql(slug)
    # if df.shape[0]>0:
    #     for x in df.values.tolist():
    #         if int(x[0].split(',')[0])<12000 and int(x[0].split(',')[1])<5000:
    #             # 垂直堆疊=原本直+新值，要記得轉成數值
    #             pointsarray = np.vstack([pointsarray,np.array([int(x[0].split(',')[0]),int(x[0].split(',')[1])])])
    # estimator = KMeans(n_clusters=n_clusters)#構造聚類器
    # estimator.fit(pointsarray)#聚類
    # label_pred = estimator.labels_ #獲取聚類標籤
    # #繪製k-means結果
    # if args["grouping"]>=1:
    #     x0 = pointsarray[label_pred == 0]
    #     plt.scatter(np.mean(x0[:, 0]), np.mean(x0[:, 1]), marker='.', label='label0')
    # if args["grouping"]>=2:
    #     x1 = pointsarray[label_pred == 1]
    #     plt.scatter(np.mean(x1[:, 0]), np.mean(x1[:, 1]), marker=',', label='label1')
    # if args["grouping"]>=3:
    #     x2 = pointsarray[label_pred == 2]
    #     plt.scatter(np.mean(x2[:, 0]), np.mean(x2[:, 1]), marker='o', label='label2')
    # if args["grouping"]>=4:
    #     x3 = pointsarray[label_pred == 3]
    #     plt.scatter(np.mean(x3[:, 0]), np.mean(x3[:, 1]), marker='v', label='label3')
    # if args["grouping"]>=5:
    #     x4 = pointsarray[label_pred == 4]
    #     plt.scatter(np.mean(x4[:, 0]), np.mean(x4[:, 1]), marker='^', label='label4')
    # if args["grouping"]>=6:
    #     x5 = pointsarray[label_pred == 5]
    #     plt.scatter(np.mean(x5[:, 0]), np.mean(x5[:, 1]), marker='<', label='label5')
    # if args["grouping"]>=7:
    #     x6 = pointsarray[label_pred == 6]
    #     plt.scatter(np.mean(x6[:, 0]), np.mean(x6[:, 1]), marker='>', label='label6')
    # if args["grouping"]>=8:
    #     x7 = pointsarray[label_pred == 7]
    #     plt.scatter(np.mean(x7[:, 0]), np.mean(x7[:, 1]), marker='1', label='label7')
    # if args["grouping"]>=9:
    #     x8 = pointsarray[label_pred == 8]
    #     plt.scatter(np.mean(x8[:, 0]), np.mean(x8[:, 1]), marker='2', label='label8')
    # plt.xlabel('petal length')
    # plt.ylabel('petal width')
    # image = r'D:\mblog\mblog\static\kmeans.png'
    # plt.savefig(image)
    # with open(image, "rb") as image_file:
    #     bas64string = "<table><base64>"+base64.b64encode(image_file.read())+"</base64></table>"
    return render(request, 'kmeans.html', locals())

def getCelodsBySql(sqlcommand =''):
    url="http://10.30.10.17:3000/RPTWebServices/L6BServices.asmx?op=GetCelODS"
    #headers = {'content-type': 'application/soap+xml'}

    headers = {'content-type': 'text/xml'}
    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <GetCelODS xmlns="http://tempuri.org/">
        <sql>"""+sqlcommand+"""</sql>
        </GetCelODS>
    </soap:Body>
    </soap:Envelope>"""
    #get data from web service
    response = requests.post(url,data=body,headers=headers)
    #decode and replace xml format string
    #if error,content '</Error></Table></DataSet></getLcmODSBySqlResult></getLcmODSBySqlResponse></soap:Body></soap:Envelope>' & '</getLcmODSBySqlResult></getLcmODSBySqlResponse></soap:Body></soap:Envelope>'
    xml_content = response.content.decode('utf-8').replace('<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><GetCelODSResponse xmlns="http://tempuri.org/"><GetCelODSResult>', '').replace('&lt;', '<').replace('&gt;', '>').replace('</GetCelODSResult></GetCelODSResponse></soap:Body></soap:Envelope>', '').replace(';','') 
    df = pd.read_xml(xml_content)
    return df