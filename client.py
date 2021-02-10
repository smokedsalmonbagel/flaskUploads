import json, time, requests,os,uuid,math
from random import randint
from uuid import uuid4
import os.path,sys,argparse


class uploadItem:
    def __init__(self,path,endpoint,data):
        self.endpoint = endpoint
        self.path = path
        self.data = data
    def read_in_chunks(self,file_object, chunk_size):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
    def upload(self):
        path = self.path
        data = self.data
        if os.path.isfile(path):
            file = path
            fid = path.split('/')[-1]
            uid = uuid.uuid4().hex
            chunk_size = 102400
            content_name = str(file)
            content_path = os.path.abspath(file)
            print(content_path)
            content_size = os.stat(content_path).st_size
            f = open(content_path,'rb')
            index = 0
            offset = 0
            headers = {}
            n=1
            fs = os.path.getsize(file)
            chunks = int(math.ceil(os.path.getsize(file)/float(chunk_size) ))
            #print fs
            #print chunks
            for chunk in self.read_in_chunks(f,chunk_size):
                offset = index + len(chunk)
                #headers['Content-Type'] = 'multipart/form-data'
                #headers['Content-length'] = str(content_size)
                #headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset, content_size)
                index = offset
                params = {'req':'upload','chunk':str(n),'chunks':str(chunks),'unique_id':fid,'uuid':uid,'chunk_size':chunk_size}
                r = requests.post(self.endpoint, files={'file':chunk},data=params)
                print(params)
                print(r.text)

                n+=1
            
            
        params = {'req':'data','payload':json.dumps(data)}
        r = requests.post(self.endpoint, data=params)
        ##print r.text

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='file to upload')
    parser.add_argument('file', type=str,
                        help='path to the file you want to upload.')
    args = parser.parse_args()
    if os.path.isfile(args.file):

        d = '''{"othermetadata":"something"}'''
        u = uploadItem(args.file,'http://127.0.0.1:5000/upload',d)
        u.upload()
    else:
        print(f"File not found {args.file}")