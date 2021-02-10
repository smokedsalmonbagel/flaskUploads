from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os,time,sys

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['TEMP_FOLDER'] = 'temp/'

@app.route("/upload", methods=["POST", "PUT"])
def upload_process():
    path = app.config['TEMP_FOLDER']
    now = time.time()
    for f in os.listdir(path):
        fp = os.path.join(path,f)
        print(fp,os.stat(fp).st_mtime,now)
        if os.path.isfile(fp) and  os.stat(fp).st_mtime < now - 60:
            os.remove(fp)
    if request.files is not None and request.form.get('uuid') is not None:
        fileuuid = request.form.get('uuid')
        chunk = request.form.get('chunk').zfill(5);
        chunks = request.form.get('chunks').zfill(5);
        tempFullPath = os.path.join(app.config['TEMP_FOLDER'], fileuuid)

        with open(tempFullPath, "ab") as f:
            file = request.files['file']
            f.write(file.stream.read())
        d = {'msg': f'chunk {chunk} / {chunks} recieved'}
        #print(chunk,chunks)
        if chunk == chunks:
            os.rename(tempFullPath, os.path.join(app.config['UPLOAD_FOLDER'], f'{fileuuid}.wav'))
            d['msg2'] = 'Upload complete'
        return jsonify(d)
    return jsonify({'msg':'no data'})
        


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)