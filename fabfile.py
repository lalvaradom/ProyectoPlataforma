import os,sys,logging
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task
from fabric.operations import local as lrun, run
from fabric.state import env
from settings import BUCKET_NAME
import data
import detector
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')


@task
def process():
    dataset = data.Dataset()
    count  = 0
    start = time.time()
    for model,key,img in dataset.get_images(BUCKET_NAME):
        print model,key,img.shape,detector.detect(img)
        count +=1
        if count == 20:
            print round(time.time() - start,1)
            break

