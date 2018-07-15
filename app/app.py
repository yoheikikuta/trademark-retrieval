from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_bootstrap import Bootstrap
import json

import tensorflow as tf
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import Model
import numpy as np
from PIL import Image as pil_image
import os
import io
import sys; sys.path.append("/faiss/python/")
import faiss
import pickle

app = Flask(__name__)
bootstrap = Bootstrap(app)

def prepare_NN_search(dict_file, idx_file):
    global idx_name_dict, faiss_idx
    with open(dict_file, 'rb') as f:
        idx_name_dict = pickle.load(f)
    faiss_idx = faiss.read_index(idx_file)

def load_model():
    global model
    base = ResNet50(weights='imagenet')
    model = Model(inputs=base.input, outputs=base.get_layer('flatten_1').output)
    global graph
    graph = tf.get_default_graph()

def preprocess_img(img_path, size=(224,224)):
    img = pil_image.open(img_path)
    img = img.resize(size)
    x = image.img_to_array(img)
    # Expand dim for handling batch dim.
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    return x

def return_topk(idx_name_dict, feature, faiss_idx, k=3):
    D, I = faiss_idx.search(feature, k)
    topk = [idx_name_dict[elem].split("/")[-1] for elem in np.squeeze(I)]

    return topk

@app.route('/')
def index():
    return render_template('img.html')

@app.route('/retrieval', methods=['POST','GET'])
def retrieval():
    query_img = request.files['img_data']
    query_img.save(os.path.join("/app/static/", "query.jpg"))
    preprocessed_img = preprocess_img(os.path.join("/app/static/", "query.jpg"))
    with graph.as_default():
        feature = model.predict(preprocessed_img)

    top3_similar_files = return_topk(idx_name_dict, feature, faiss_idx)

    # Return answer
    return render_template("img.html"
            , query_url="query.jpg"
            , img_url1=top3_similar_files[0]
            , img_url2=top3_similar_files[1]
            , img_url3=top3_similar_files[2])

@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory("/app/static/", filename)


if __name__ == "__main__":
    load_model()
    prepare_NN_search('/app/trained_index/2017-jpeg.pickle', "/app/trained_index/2017-jpeg.index")
    app.run(host='0.0.0.0',port=5000,debug=True)
