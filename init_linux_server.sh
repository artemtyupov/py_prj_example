echo git username: && \
read username && \

echo git password: && \
read password && \

git clone https://${username}:${password}@gitlab.com/tyupovartem/wb.git && \

echo Updating...  && \
sudo apt-get update && \
sudo apt update && \

echo Installing...  && \
sudo apt-get -y install docker && \
sudo apt -y install docker-compose && \

echo Setting permissions...  && \
sudo chmod 666 /var/run/docker.sock && \

cd wb && \
sudo chmod +x ./start.sh && \
sudo chmod +x ./end.sh && \

echo Starting docker...  && \
./start.sh