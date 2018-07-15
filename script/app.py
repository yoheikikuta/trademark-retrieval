from flask import Flask, jsonify, request
import json

import tensorflow as tf
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import Model
import numpy as np
from PIL import Image as pil_image
import io
import sys; sys.path.append("/faiss/python/")
import faiss
import pickle

app = Flask(__name__)

def prepare_NN_search(dict_file, idx_file):
    global idx_name_dict, faiss_idx
    with open(dict_file, 'rb') as f:
        idx_name_dict = pickle.load(f)
    faiss_idx = faiss.read_index(idx_file)

def load_model():
    global model
    #model = FeatureExtractor()
    base = ResNet50(weights='imagenet')
    model = Model(inputs=base.input, outputs=base.get_layer('flatten_1').output)
    global graph
    graph = tf.get_default_graph()

def preprocess_img(img_byte, size=(224,224)):
    img = pil_image.open(io.BytesIO(img_byte))
    img = img.resize(size)
    x = image.img_to_array(img)
    # Expand dim for handling batch dim.
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    return x

def return_topk(idx_name_dict, feature, faiss_idx, k=3):
    D, I = faiss_idx.search(feature, k+1)
    topk = [idx_name_dict[elem] for elem in np.squeeze(I)]

    return topk[1:]

@app.route('/app/image', methods=['POST'])
def retrieval():
    preprocessed_img = preprocess_img(request.files['image'].read())
    with graph.as_default():
        feature = model.predict(preprocessed_img)

    top3_similar_files = return_topk(idx_name_dict, feature, faiss_idx)
    result = {
      "Result":{"shape": top3_similar_files}
    }
    # Return answer
    return jsonify(result)


if __name__ == "__main__":
    load_model()
    prepare_NN_search('/app/trained_index/2017-jpeg.pickle', "/app/trained_index/2017-jpeg.index")
    app.run(host='0.0.0.0',port=5000,debug=True)
