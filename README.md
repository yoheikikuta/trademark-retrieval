# trademark-retrieval

This is a repository for trying US trademark image retrieval.

## Collect data and Create index for retrieval

```
git clone https://github.com/yoheikikuta/trademark-retrieval.git
cd trademark-retrieval
docker build -t [image tag] -f Dockerfile .
docker run --rm -it -v $PWD:/work -p 8888:8888 [image tag]
```

In the caintainer, execute the following commands to download data and create index.

```
python script/download-trademark-images.py
python script/create-index.py
```

In a CPU environment, it takes about ten minutes to the downloading and about 1.5 horus to the indexing.


## Launch Web app

```
docker build -t [app image tag] -f Dockerfile.app .
docker run --rm -it -v $PWD/data/images:/app/static -p 5000:5000 [app image tag]
```

Visit `localhost:5000` on your local browser and upload a query image.


## Screenshot

![screenshot](https://github.com/yoheikikuta/trademark-retrieval/blob/images/screenshot.png)
