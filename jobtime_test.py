import time
import requests
import re
from datadog import initialize, statsd
# import google.cloud.logging
import logging
import os


def main():
    # logging.warning("start logging")
    # host=os.environ.get('AGENT_HOST')
    # logging.warning(host)
    # options = {
    # 'statsd_host': host,
    # 'statsd_port':8125
    # }
    # initialize(**options)

    i=0
    l1,l2=getInfo()
    for s in l1:
        ns,jn=getjn(s)
        for s2 in l2:
            ns2,jn2=getjn(s2)
            if ns==ns2 and jn==jn2:
                starttime=s2.split(' ')[1]
                now=time.time()
                uptime=now-float(starttime)
                print(ns + "   " + jn + "   " + str(uptime))
        
        # starttime=line.split(' ')[1]
    # for s in l2:
    #     print(s)
    # while (1):
    #     #i+=1
    #     ut,ns,jn=getInfo()
    #     if ut!=0 and jn!="":
    #         # statsd.gauge('job_uptime', ut, tags=["namespace:"+ns,"jobname:"+jn])
    #         print(jn)
    #     time.sleep(15)
        #if i>10:
            #break

def getInfo():
    # print("start getInfo")
    #please replace the pod ip
    # res=requests.get('http://10.244.1.7:8080/metrics')
    # print("getRes")
    namespace=""
    jobname=""
    starttime=0
    f=open('metric.txt')
    # lines=f.readlines()
    listActiveJob=[]
    listStartTime=[]
    for line in f.readlines():
        # print line
        # print(line)
        if line.startswith('kube_job_status_active') and line.rstrip().endswith("1"):
            namespace, jobname=getjn(line)
            listActiveJob.append(line)
            # print(jobname)
        if line.startswith('kube_job_status_start_time'):
            listStartTime.append(line)
            # ns, jn=getjn(line)
            # if jn==jobname and ns==namespace:
            #     starttime=line.split(' ')[1]

    # now=time.time()
    # uptime=now-float(starttime)
    # return uptime,namespace,jobname
    return listActiveJob,listStartTime

def getjn(s):
    ns=re.findall(r'namespace="(.+?)"',s)[0]
    jn=re.findall(r'job_name="(.+?)"',s)[0]
    return ns,jn

def test():
    print("it is a test")
    f=open('metric.txt')
    lines=f.readlines()
    linecount=0
    for line in lines:
        linecount=linecount+1
        print(line)
    f.close()
    print(linecount)


if __name__ == '__main__':
    main()
    # test()