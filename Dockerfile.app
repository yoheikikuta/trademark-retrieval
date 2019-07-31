FROM ubuntu:18.04
LABEL maintainer="diracdiego@gmail.com"
LABEL version="1.0"

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
    jupyter \
    numpy \
    tqdm \
    pillow \
    tensorflow==1.10.0 \
    h5py \
    keras==2.2.2

RUN ln -s /usr/bin/python3.6 /usr/bin/python

WORKDIR /
RUN git clone https://github.com/yoheikikuta/faiss.git
WORKDIR /faiss
RUN ./configure
RUN sed -i -e "s/PYTHONCFLAGS =  -I\/usr\/lib\/python3\/dist-packages\/numpy\/core\/include/PYTHONCFLAGS =  -I\/usr\/include\/python3.6\/ -I\/usr\/lib\/python3\/dist-packages\/numpy\/core\/include/g" makefile.inc
RUN make && make install && make py

RUN pip install \
    flask \
    flask-bootstrap

ARG project_dir=/app/
ADD ./app/ $project_dir
WORKDIR $project_dir
ADD ./data/trained_index/ /app/trained_index/

CMD ["python", "app.py"]
