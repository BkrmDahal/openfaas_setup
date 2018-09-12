echo "set variables "
IP="142.93.197.8"

echo "Get openfaas from github"
git clone https://github.com/openfaas/faas

echo "start the swarm"
docker swarm init --advertise-addr $IP

echo "deploy openfass"
cd faas && ./deploy_stack.sh --no-auth

echo "get openfaas cli"
curl -sSL https://cli.openfaas.com | sudo sh

echo "Make new folder"
mkdir -p functions && \
  cd functions
  
echo "make new funcation templates"
faas-cli new --lang python article_tag
