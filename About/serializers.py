from rest_framework import serializers
import requests
import base64
import matplotlib.pyplot as plt
import pandas as pd 

class matpshow(serializers.ModelSerializer):


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
