# trademark-retrieval

This is a repository for trying US trademark image retrieval.

## Collect data and Create index for retrieval

```
git clone https://github.com/yoheikikuta/trademark-retrieval.git
cd trademark-retrieval
docker build -t [image tag] -f Dockerfile .
docker run --rm -it -v $PWD:/work -p 8888:8888 [image tag]
```

In the caintainer,

```
python script/download-trademark-images.py
python script/create-index.py
```

## Launch Web app

```
docker build -t [app image tag] -f Dockerfile.app .
docker run --rm -it -v $PWD/data/images:/app/static -p 5000:5000 [app image tag]
```

Visit `localhost:5000` on your local browser and upload a query image.
