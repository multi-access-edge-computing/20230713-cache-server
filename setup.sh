mkdir /home/redis-data
sudo yum update -y
sudo yum install docker python3 python3-pip -y
docker volume create redis-volume
docker run --name cache-server -p 6379:6379 -v redis-volume:/home/redis-data -d redis redis-server --appendonly yes
pip3 install --upgrade pip
pip3 install boto3 redis
