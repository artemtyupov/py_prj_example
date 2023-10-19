#BASEDIR=$(dirname "$0")
#
#cd $BASEDIR/database_service
#pipreqs --f --encoding=utf8 .
#cd ../excel_service
#pipreqs --f --encoding=utf8 .
#cd ../parsing_service
#pipreqs --f --encoding=utf8 .
#cd ../updater_service
#pipreqs --f --encoding=utf8 .
#
#cd ..

OUTPUT=$(docker network ls --filter name=CustomDockerNetwork)
if [[ ! "$OUTPUT" =~ "CustomDockerNetwork" ]]; then
  docker network create CustomDockerNetwork
fi

docker volume create dbtuto
docker-compose build
docker-compose up -d