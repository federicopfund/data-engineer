
sudo usermod -aG fede $USER
sudo service docker restart
sudo chown $USER:$USER docker-compose.yml
sudo chmod 666 /var/run/docker.sock
groups

