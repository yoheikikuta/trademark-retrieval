#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import Model
import numpy as np
import glob
import os
import sys; sys.path.append("/faiss/python/")
import faiss
import pickle
from tqdm import tqdm

datadir = "/work/data/"
savedir = os.path.join(datadir, "trained_index")
feature_dim = 2048
saveindexpath = os.path.join(savedir, "2017-jpeg.index")
saveindexinfopath = os.path.join(savedir, "2017-jpeg.pickle")


class FeatureExtractor(object):

    def __init__(self, extract_layer='flatten_1'):
        self.base = ResNet50(weights='imagenet')
        self.model = Model(inputs=self.base.input, outputs=self.base.get_layer(extract_layer).output)

    def img_preprocess(self, img_path, size=(224,224)):
        img = image.load_img(img_path, target_size=size)
        x = image.img_to_array(img)
        # Expand dim for handling batch dim.
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        return x

    def extract_feature(self,img_path):
        x = self.img_preprocess(img_path)
        feature = self.model.predict(x)

        return feature


def compute_features(feature_extractor, fpath_list):
    total_num = len(fpath_list)
    # Initiaize features matrix.
    features = np.eye(total_num, feature_dim)

    for idx, fpath in tqdm(enumerate(fpath_list)):
        fname = os.path.basename(fpath)
        feature = feature_extractor.extract_feature(fpath)
        feature = np.squeeze(feature)
        features[idx,:] = feature

    # Change data type for indexing of faiss.
    features = features.astype('float32')

    return features


def create_and_save_faiss_index(features, fpath_list):
    index = faiss.IndexFlatL2(feature_dim)
    index.add(features)
    faiss.write_index(index, saveindexpath)

    index_filename_dict = {}

    for idx,f in enumerate(fpath_list):
        index_filename_dict[idx] = f

    with open(saveindexinfopath, 'wb') as f:
        pickle.dump(index_filename_dict, f, protocol=pickle.HIGHEST_PROTOCOL)


def main():
    os.makedirs(savedir, exist_ok=True)

    if os.path.isfile(saveindexinfopath):
        print("Files already exist.")
        return

    model = FeatureExtractor()
    fpath_list = glob.glob(os.path.join(datadir, "images/*.jpg"))
    print("Total {} jpeg images".format(len(fpath_list)))

    features = compute_features(model, fpath_list)
    create_and_save_faiss_index(features, fpath_list)

    print("Finished indexing and save trained index.")


if __name__ == '__main__':
    main()
