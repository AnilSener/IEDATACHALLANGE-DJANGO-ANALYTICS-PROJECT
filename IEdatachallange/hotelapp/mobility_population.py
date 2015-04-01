# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 01:08:27 2015

@author: root
"""
import pandas as pd
import os
import datetime
import pymongo
"""client = pymongo.MongoClient('localhost', 27017)
db = client['hotelapp']
collection = db['telefonica_population']"""
from hotelapp.models import TelefonicaPopulation,TelefonicaMap
import configparser

config = configparser.ConfigParser()
config.read('../app.conf')
from mongoengine.connection import connect,disconnect


parse = lambda x,y: datetime.datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]),int(y))
def getPopulation(date,hour):
    connection=connect(config["MONGODB"]["DB_NAME"])
    #dfPopulation=pd.read_csv("data/telefonica/cleaned_mobile_data/"+str(date)+".csv",header=False,names=["date","cell_id","hour","n_people"],index_col=["date","hour"])
    #dfPopulation=pd.read_csv("data/telefonica/cleaned_mobile_data/"+str(date)+".csv",header=False,names=["date","cell_id","hour","n_people"],parse_dates={"date_time" : [0,2]}, date_parser=parse,index_col=0)
    #cursor=collection.find({"date": str(date)})

    #for item in cursor:
    #    items.append(item)
    qs=TelefonicaPopulation.objects.filter(date=str(date),hour=hour)
    popn=qs[:1].get()
    #disconnect()
    #dfPopulation.index=pd.to_datetime(dfPopulation["date"]+)
    return popn

def getPopulationAllDays():
    dfPopulation=pd.DataFrame(columns=["date","cell_id","hour","n_people"])
    docs = os.popen("""ls """+config["DEFAULT"]["DC_BASE_DIR"]+"""data/telefonica/cleaned_mobile_data/*.csv|awk 'BEGIN{FS="/"}{print $NF}'""").readlines()
    for doc in docs:
        dfPopulation=pd.concat([dfPopulation,pd.read_csv("data/telefonica/cleaned_mobile_data/"+doc[:-1],header=False,names=["date","cell_id","hour","n_people"], parse_dates={"date_time" : [0,2]},date_parser=parse,index_col=0)])
    return dfPopulation

#print(getPopulation("2014-01-02",8))

#print(getPopulationAllDays())
#getPopulationAllDays()



retval=None
import shlex, subprocess
#CSV to JSON Conversion
def storePopulation():
    docs = os.popen("""ls """+config["DEFAULT"]["DC_BASE_DIR"]+"""data/telefonica/cleaned_mobile_data/*.csv|awk 'BEGIN{FS="/"}{print $NF}'""").readlines()

    for doc in docs:
        command_line = config["MONGODB"]["BASE_DIR"]+"mongoimport -d "+config["MONGODB"]["DB_NAME"]+" --username "+config["MONGODB"]["USER_NAME"]+" --password "+config["MONGODB"]["PASSWORD"]+" --type csv -c telefonica_population  -f date,cell_id,hour,n_people --file "+config["DEFAULT"]["DC_BASE_DIR"]+"data/telefonica/cleaned_mobile_data/"+doc[:-1]
        args = shlex.split(command_line)
        print(args)
        p = subprocess.Popen(command_line, shell=True) # Success!
        """lines=None
        try:
            lines=p.stdout.readlines()
        except AttributeError:
          pass

        for line in lines:
            print(line)"""
        retval = p.wait()
        """if retval:
            print(doc+" inserted to mongodb.")
            continue;
        else:
            print(doc+" cannot be inserted to mongodb.")
            break;"""
storePopulation()

"""def updateMapCellIdKey():
    pops=TelefonicaPopulation.objects.all()
    for pop in pops:
        TelefonicaMap.objects(properties__cell_id=pop.cell_id).get()"""