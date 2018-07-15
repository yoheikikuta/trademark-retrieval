FROM ubuntu:17.10
MAINTAINER Yohei Kikuta <diracdiego@gmail.com>

RUN apt-get update

RUN apt-get install -y \
    python3.6 \
    python3-pip \
    python3-dev \
    python3-numpy \
    git \
    curl \
    libblas-dev \
    liblapack-dev

RUN pip3 install --upgrade pip

RUN pip install \
    numpy \
    pillow \
    tensorflow \
    h5py \
    keras \
    flask

RUN ln -s /usr/bin/python3.6 /usr/bin/python

WORKDIR /
RUN git clone -b fix-test-tmpfile https://github.com/yoheikikuta/faiss.git
WORKDIR /faiss
RUN ./configure
RUN sed -i -e "s/PYTHONCFLAGS =  -I\/usr\/lib\/python3\/dist-packages\/numpy\/core\/include/PYTHONCFLAGS =  -I\/usr\/include\/python3.6\/ -I\/usr\/lib\/python3\/dist-packages\/numpy\/core\/include/g" makefile.inc
RUN make && make install && make py

ARG project_dir=/app/
ADD ./script/app.py $project_dir
WORKDIR $project_dir
ADD ./data/trained_index/ /app/trained_index/

CMD ["python", "app.py"]
