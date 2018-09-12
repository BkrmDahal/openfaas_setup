# install docker
# docker run -d -p 3000:3000 grafana/grafana

echo "install grafana"
curl https://packagecloud.io/gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://packagecloud.io/grafana/stable/debian/ stretch main"
sudo apt-get update
sudo apt-get install grafana
sudo systemctl status grafana-server
sudo systemctl enable grafana-server
