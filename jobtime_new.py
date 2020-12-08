import time
import datetime
import requests
import re
from datadog import initialize, statsd
# import google.cloud.logging
import logging
import os
from kubernetes import client, config
import kubernetes
from _datetime import timezone

def main():
    options = {
    'statsd_host': '127.0.0.1',
    'statsd_port':8125
    }
    initialize(**options)

    while (1):
        job,duration=getJob()
        if job!=None:
            print(job.metadata.name)
            print(duration)
            statsd.gauge('job_duration', duration, tags=["namespace:"+job.metadata.namespace,"jobname:"+job.metadata.name])
        time.sleep(10)
        
    
def getJob():
    config.load_kube_config()
    api_instance=client.BatchV1Api()
    jobs=api_instance.list_namespaced_job(namespace='default',
                                        # async_req=True,
                                        pretty=True,
                                        timeout_seconds=60)
    for job in jobs.items:
        if job.status.active==1:
            now=datetime.datetime.now(timezone.utc)
            # print(job.status.start_time)
            duration=int((now-job.status.start_time).total_seconds())
            return job, duration
    return None,0
            # m=int(duration/60)
            # s=duration % 60

            # print("%s\t%s\t%s\t%s" % (job.metadata.namespace, job.metadata.name,str(duration),str(m)+"m"+str(s)+"s"))

def test():
    options = {
    'statsd_host': 'localhost',
    'statsd_port':8125
    }
    initialize(**options)
    while (1):
        statsd.gauge('job_test', 200, tags=["namespace:a","jobname:b"])
        time.sleep(5)

if __name__ == '__main__':
    main()
    # test()