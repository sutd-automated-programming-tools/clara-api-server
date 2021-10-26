cd /clara-api-server
echo 'adding path to .bashrc'
# shellcheck disable=SC2016
echo 'export LD_LIBRARY_PATH=/usr/lib/lp_solve/
export PATH=$PATH:/home/ubuntu/.local/bin'>>~/.bashrc
. ~/.bashrc
echo 'get update'
apt-get update
echo 'install pip'
apt-get -y install python3-pip
/usr/local/bin/python -m pip install --upgrade pip
echo 'install aptitude'
apt-get install -y aptitude
echo 'install lpsolve'
aptitude install -y lp-solve liblpsolve55-dev
echo 'install pip requirements'
pip3 install -r requirements.txt
echo 'execute make'
make
echo 'launch traefik proxy server'
nohup ./traefik --configFile=traefik.toml &> /dev/null &
echo 'launching  server at:'
uvicorn main:app  --host 0.0.0.0 
echo $(curl ifconfig.me 2>/dev/null)/clara/
