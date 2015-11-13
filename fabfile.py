import os,sys,logging
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task
from fabric.operations import local as lrun, run
from fabric.state import env
from settings import BUCKET_NAME
import data

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')


@task
def process():
    dataset = data.Dataset()
    for model,key,img in dataset.get_images(BUCKET_NAME):
        print model,key,img.shape
        break

