import time
import requests
import re
from datadog import initialize, statsd
# import google.cloud.logging
import logging
import os


def main():
    logging.warning("start logging")
    host=os.environ.get('AGENT_HOST')
    logging.warning(host)
    options = {
    'statsd_host': host,
    'statsd_port':8125
    }
    initialize(**options)

    
    # logging.warning(st)
    # logging.warning(ns)
    # logging.warning(jn)
    #testgetInfo()
    #print(st)
    i=0
    while (1):
        #i+=1
        st,ns,jn=getInfo()
        if st!=0 and jn!="":
            statsd.gauge('job_uptime', st, tags=["namespace:"+ns,"jobname:"+jn])
        time.sleep(15)
        #if i>10:
            #break

def testgetInfo():
    now=time.time()
    starttime='1.607067512e+09'
    returnValue=now - float(starttime)
    print(returnValue)

def getInfo():
    print("start getInfo")
    #please replace the pod ip
    res=requests.get('http://10.244.0.5:8080/metrics')
    print("getRes")
    namespace=""
    jobname=""
    starttime=0
    for line in res.text.splitlines():
        # print line
        if line.startswith('kube_job_status_active') and line.endswith('1'):
            namespace, jobname=getjn(line)
            print(jobname)
        if line.startswith('kube_job_status_start_time'):
            if jobname=="":
                return 0,None,None
            ns, jn=getjn(line)
            if jn==jobname and ns==namespace:
                starttime=line.split(' ')[1]

    #print(namespace)
    #print(jobname)
    #print(starttime)

    now=time.time()
    uptime=now-float(starttime)
    return uptime,namespace,jobname

def getjn(s):
    ns=re.findall(r'namespace="(.+?)"',s)[0]
    jn=re.findall(r'job_name="(.+?)"',s)[0]
    return ns,jn

if __name__ == '__main__':
    main()