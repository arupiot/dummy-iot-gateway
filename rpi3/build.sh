sudo docker build -t dummy-gateway ../
sudo docker images
sudo docker tag dummy-gateway arupiot/dummy-gateway:demo
sudo docker push arupiot/dummy-gateway:demo