from django.shortcuts import render
from django.http import HttpResponse,Http404
from mainsite.models import Product
import requests
import random
# Importing the libraries
import base64
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import csv
from io import BytesIO
from PIL import Image
import io
# Importing the dataset 
from sklearn.cluster import KMeans
# Create your views here.

def about(request):
    quotes = ['今日事,今日畢',
            '怎麼收穫,怎麼栽',
            '知識就是力量',
            '一個人的個性就是他的命運']
    quote = random.choice(quotes)
    return render(request,'about.html',locals())

def listing(request):
    products = Product.objects.all()
    return render(request,'list.html',locals())

def disp_detail(request,id):
    try:
        p= Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404('找不到指定的品項編號')
    return render(request,'disp.html',locals())

def matpshow(request,slug):
    pointsarray = np.array([0,0])
    df=getCelodsBySql(slug)
    if df.shape[0]>0:
        plt.rcParams["figure.figsize"] = (4,4)
        for idx,row in df.iterrows():
            pointsarray = np.vstack([pointsarray,np.array([int(row[0]),int(row[1])])])
        plt.scatter((pointsarray[:, 0]), (pointsarray[:, 1]))
        plt.xlabel('petal length')
        plt.ylabel('petal width')
        image = r'D:\mblog\mblog\static\plot.png'
        plt.savefig(image)
        # plt.switch_backend('agg')
        # image.seek(0)
        with open(image, "rb") as image_file:
            pic_hash = base64.b64encode(image_file.read())
    else:
        pic_hash=slug
        # for x in df.values.tolist():
        #     if int(x[0].split(',')[0])<12000 and int(x[0].split(',')[1])<5000:
        #         # 垂直堆疊=原本直+新值，要記得轉成數值
        #         pointsarray = np.vstack([pointsarray,np.array([int(x[0].split(',')[0]),int(x[0].split(',')[1])])])
    # with open('deft.csv', newline='') as csvfile:
    #     rows = csv.reader(csvfile)
    #     for row in rows:
    #         if int(row[0])<12000 and int(row[1])<5000:
    #             pointsarray = np.vstack([pointsarray,np.array([int(row[0]),int(row[1])])])
    # X=pointsarray
    # wcss = [] 
    # for i in range(1, 11): 
    #     kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    #     kmeans.fit(X) 
    #     wcss.append(kmeans.inertia_)
    # # Using the elbow method to find the optimal number of clusters wcss = [] for i in range(1, 11): 
    # wcss.append(kmeans.inertia_)
    # image = r'D:\mblog\mblog\static\plot.png'
    # plt.plot(range(1, 12), wcss) 
    # plt.xlabel('Number of clusters') 
    # plt.ylabel('WCSS') 
    # plt.savefig(image)
    # # image.seek(0)
    # with open(image, "rb") as image_file:
    #     pic_hash = base64.b64encode(image_file.read())
    #     with open(r'D:\mblog\mblog\static\temp.png', "wb") as fh:
    #         fh.write(base64.decodebytes(pic_hash))
    # # plt.imshow(img)
    # # plt.show()
    return render(request, 'matplotlib.html', locals())

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