docker container stop python-container

docker container rm python-container

docker build --tag python-docker .

docker run --name python-container -d -p 5000:5000 python-docker