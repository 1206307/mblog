from django.shortcuts import render
from django.http import HttpResponse,Http404
from mainsite.models import Product
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

def matpshow(request):
    pointsarray = np.array([0,0])
    with open('deft.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if int(row[0])<12000 and int(row[1])<5000:
                pointsarray = np.vstack([pointsarray,np.array([int(row[0]),int(row[1])])])
    X=pointsarray
    wcss = [] 
    for i in range(1, 11): 
        kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
        kmeans.fit(X) 
        wcss.append(kmeans.inertia_)
    # Using the elbow method to find the optimal number of clusters wcss = [] for i in range(1, 11): 
    wcss.append(kmeans.inertia_)
    image = r'D:\mblog\mblog\static\plot.png'
    plt.plot(range(1, 12), wcss) 
    plt.xlabel('Number of clusters') 
    plt.ylabel('WCSS') 
    plt.savefig(image)
    # image.seek(0)
    with open(image, "rb") as image_file:
        pic_hash = base64.b64encode(image_file.read())
        with open(r'D:\mblog\mblog\static\temp.png', "wb") as fh:
            fh.write(base64.decodebytes(pic_hash))
    # plt.imshow(img)
    # plt.show()
    return render(request, 'matplotlib.html', locals())