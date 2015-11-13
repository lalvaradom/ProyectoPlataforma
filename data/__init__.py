import os,time,random
from collections import defaultdict
import gzip


class Dataset:
    def __init__(self):
        self.models = defaultdict(list)
        for line in gzip.GzipFile(os.path.join(os.path.dirname(__file__),"data.txt.gz")):
            try:
                date,time,size,key = line.strip().split()
                _,name,fname = key.split('/')
                self.models[name].append({'key':key,'size':int(size)})
            except:
                print line

    def print_sorted(self):
        for k,v in sorted([ (len(v),k) for k,v in self.models.iteritems()],reverse=True):
            print k,v


if __name__ == "__main__":
    d = Dataset()
    print len(d.models)