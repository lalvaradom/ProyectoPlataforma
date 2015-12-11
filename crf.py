# -*- coding: utf-8 -*-
"""
This package contains code for the "CRF-RNN" semantic image segmentation method, published in the
ICCV 2015 paper Conditional Random Fields as Recurrent Neural Networks. Our software is built on
top of the Caffe deep learning library.

Contact:
Shuai Zheng (szheng@robots.ox.ac.uk), Sadeep Jayasumana (sadeep@robots.ox.ac.uk), Bernardino Romera-Paredes (bernard@robots.ox.ac.uk)

Supervisor:
Philip Torr (philip.torr@eng.ox.ac.uk)

For more information about CRF-RNN, please vist the project website http://crfasrnn.torr.vision.
"""

caffe_root = '../caffe-crfrnn/'
import sys
import time
sys.path.insert(0, caffe_root + 'python')

import os,glob
import cPickle
import logging
import numpy as np
import pandas as pd
from PIL import Image as PILImage
#import Image
import cStringIO as StringIO
import caffe
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


MODEL_FILE = 'TVG_CRFRNN_COCO_VOC.prototxt'
PRETRAINED = 'TVG_CRFRNN_COCO_VOC.caffemodel'
IMAGE_FILE = 'input.jpg'


#caffe.set_mode_gpu()
pallete = [0,0,0,
            128,0,0,
            0,128,0,
            128,128,0,
            0,0,128,
            128,0,128,
            0,128,128,
            128,128,128,
            64,0,0,
            192,0,0,
            64,128,0,
            192,128,0,
            64,0,128,
            192,0,128,
            64,128,128,
            192,128,128,
            0,64,0,
            128,64,0,
            0,192,0,
            128,192,0,
            0,64,128,
            128,64,128,
            0,192,128,
            128,192,128,
            64,64,0,
            192,64,0,
            64,192,0,
            192,192,0]
net = caffe.Segmenter(MODEL_FILE, PRETRAINED)


for fname in glob.glob("data/*.jpg"):
    input_image = 255 * caffe.io.load_image(fname)
    width,height = input_image.shape[0],input_image.shape[1]
    maxDim = max(width,height)
    image = PILImage.fromarray(np.uint8(input_image))
    image = np.array(image)
    mean_vec = np.array([103.939, 116.779, 123.68], dtype=np.float32)
    reshaped_mean_vec = mean_vec.reshape(1, 1, 3)
    # Rearrange channels to form BGR
    im = image[:,:,::-1]
    # Subtract mean
    im = im - reshaped_mean_vec
    # Pad as necessary
    cur_h, cur_w, cur_c = im.shape
    pad_h = 500 - cur_h
    pad_w = 500 - cur_w
    im = np.pad(im, pad_width=((0, pad_h), (0, pad_w), (0, 0)), mode = 'constant', constant_values = 0)
    # Get predictions
    start = time.time()
    segmentation = net.predict([im])
    segmentation2 = segmentation[0:cur_h, 0:cur_w]
    print "{}\t{}".format(fname,time.time()-start)
    output_im = PILImage.fromarray(segmentation2)
    output_im.putpalette(pallete)
    output_im.save("output/{}.png".format(fname.split('/')[1].split('.')[0]))
