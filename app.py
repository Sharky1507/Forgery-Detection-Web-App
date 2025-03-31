from flask import Flask, request, render_template, g, jsonify
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import hashlib

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


SSIM_THRESHOLD = 0.9 # Feel Free to change this
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods = ['POST'])
def upload():
    if 'file1' in request.files and 'file2' in request.files:
        g.file1= request.files['file1']
        g.file2 = request.files['file2']
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        g.file1.save(os.path.join(app.config['UPLOAD_FOLDER'],g.file1.filename))
        g.file2.save(os.path.join(app.config['UPLOAD_FOLDER'],g.file2.filename))


    else:
        
        return jsonify({'error': 'Upload Two Images for Similarity check'}),400

    flag = False
    if calculate_similarity:
        if cal_md5():
            msg = "The uploaded images are not forged"
        else:
            msg = "forgery found!"
    else:
        msg = "forgery found!"
    return jsonify({'message' : msg,'flag':flag})

    return

def calculate_hash(file_path):
    with open(file_path, "rb") as file:
        md5_hash = hashlib.md5()
        while chunk := file.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def cal_md5():
    file_path1 = os.path.join(UPLOAD_FOLDER,g.file1.filename)
    file_path2 = os.path.join(UPLOAD_FOLDER,g.file2.filename)
    hash1= calculate_hash(file_path1)
    hash2 = calculate_hash(file_path2)
    if hash1 == hash2:
        return True
    return False

def calculate_similarity():
    image1path = os.path.join(UPLOAD_FOLDER,g.file1.filename)
    image2path = os.path.join(UPLOAD_FOLDER,g.file2.filename)
    image1 = cv2.imread(image1path,cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2path,cv2.IMREAD_GRAYSCALE)
    image1_resize = cv2.resize(image1,(image2.shape[1],image2.shape[0]))
    ssim_score = ssim(image1_resize,image2)
    if ssim_score>SSIM_THRESHOLD:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
