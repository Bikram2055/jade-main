#!/bin/bash

sudo apt-get update -y
sudo apt install jq -y
sudo apt install git -y
sudo apt install unzip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm awscliv2.zip
sudo git clone https://github.com/Bikram2055/jade-main.git
sudo chown -R $USER:$USER jade/
cd jade
# get secrets from parameter store and export them as environemt variable
parameter_name="jade_dev_settings"
JSON_VARS=$(aws ssm get-parameter --name "${parameter_name}" --region us-east-1 --with-decrypt | jq -r '.Parameter["Value"]')
ENV_VARS=$(jq -r 'to_entries[] | .key + "=" + .value' <<< $JSON_VARS)
eval $ENV_VARS
# write environements variables to .env
echo "$ENV_VARS" > .env
# export env variables for database for postgres docker image
POSTGRES_DB=$DB_NAME
POSTGRES_USER=$DB_USER
POSTGRES_PASSWORD=$DB_PASSWORD
# append database environment variable to .env
echo "POSTGRES_DB=$POSTGRES_DB" >> .env
echo "POSTGRES_USER=$POSTGRES_USER" >> .env
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env
sudo apt-get install docker.io -y
sudo groupadd docker
sudo usermod -aG docker $USER
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
sudo systemctl restart docker
newgrp docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose -f ./docker-compose-prod.yml build
docker-compose -f ./docker-compose-prod.yml up -d