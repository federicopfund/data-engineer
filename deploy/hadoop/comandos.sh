docker exec -it namenode hadoop fs -mkdir /user
docker exec -it namenode hadoop fs -mkdir /user/fede
docker exec -it namenode hadoop fs -mkdir /user/fede/landing
docker exec -it namenode hadoop fs -mkdir /user/fede/landing/csv
docker exec -it namenode hadoop fs -chmod 777 /user/fede/landing/csv
docker exec -it namenode hadoop fs -chown fede:hadoop /user/fede/landing/csv
