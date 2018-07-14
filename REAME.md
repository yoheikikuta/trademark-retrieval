# trademark-retrieval

This is a repository for trying US trademark image retrieval.

```
git clone https://github.com/yoheikikuta/trademark-retrieval.git
cd trademark-retrieval
docker build -t [image tag] -f Dockerfile .
docker run --rm -it $PWD:/work -v 8888:8888 [image tag]
```
