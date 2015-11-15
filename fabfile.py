import os,sys,logging
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get
from fabric.operations import local as lrun, run
from fabric.state import env
from settings import BUCKET_NAME
import data
import detector
import time
import cv2
from settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')


@task
def process():
    dataset = data.Dataset()
    for model,key,img in dataset.get_images(BUCKET_NAME):
        print model,key,img.shape,detector.detect(img)


@task
def notebook_server():
    """
    Run IPython notebook on an AWS server
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")
    c = get_config()
    c.NotebookApp.open_browser = False
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
    c.NotebookApp.enable_mathjax = False
    c.NotebookApp.password = u'{}'
    :return:
    """
    from IPython.lib.security import passwd
    sudo("/home/ubuntu/anaconda/bin/ipython notebook --ip=0.0.0.0  --NotebookApp.password={} --no-browser".format(passwd())) #--certfile=mycert.pem


@task
def notebook():
    """
    deactivate
    pip freeze > requirements.txt
    local("sudo port select --set python python27")
    local("sudo port select --set ipython ipython27")
    local("sudo port select --set pip pip27")
    local("sudo port select --set virtualenv virtualenv27")
    :return:
    """
    local("ipython-2.7 notebook")



@task
def freeze():
    local("source ~/portenv/bin/activate;pip freeze >> requirements.txt")


@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()

@task
def backup():
    get("workspace/*","workspace")

@task
def upload():
    try:
        sudo("rm -rf workspace")
        run("mkdir workspace")
    except:
        pass
    put("*.py","workspace/")
    put("*.md","workspace/")
    put("*.ipynb","workspace/")
    put("*.sh","workspace/")
    for d in filter(os.path.isdir, os.listdir('.')):
        if not d.startswith('.'):
            put("{}".format(d),"workspace/")

