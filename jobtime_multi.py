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
        jobs=getJobs()
        if jobs!=None:
            for job in jobs.items:
                if job.status.active==1:
                    now=datetime.datetime.now(timezone.utc)
                    duration=int((now-job.status.start_time).total_seconds())
                    print(job.metadata.name + ": " + str(duration))
                    # print(duration)
                    statsd.gauge('job_duration', duration, tags=["namespace:"+job.metadata.namespace,"jobname:"+job.metadata.name])
        time.sleep(10)
        

def getJobs():
    config.load_kube_config()
    api_instance=client.BatchV1Api()
    jobs=api_instance.list_namespaced_job(namespace='default',
                                        # async_req=True,
                                        pretty=True,
                                        timeout_seconds=60)
    return jobs

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

if __name__ == '__main__':
    main()