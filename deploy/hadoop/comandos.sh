docker exec -it namenode hadoop fs -mkdir /user/fede/landing
hadoop fs -chmod 777 /user/fede/landing/csv
hadoop fs -chown fede:hadoop /user/fede/landing/csv
