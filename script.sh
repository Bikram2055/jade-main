#!/bin/bash
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
cp -a /home/ubuntu/jade/. .
ls -al
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d