echo 'adding path to .bashrc'
echo 'export LD_LIBRARY_PATH=/usr/lib/lp_solve/
export PATH=$PATH:/home/ubuntu/.local/bin'>>../.bashrc
. ../.bashrc
echo 'get update'
sudo apt-get update
echo 'install pip'
sudo apt-get -y install python3-pip
echo 'install aptitude'
sudo apt-get install -y aptitude
echo 'install lpsolve'
sudo aptitude install -y lp-solve liblpsolve55-dev
echo 'install pip requirements'
pip install -r requirements.txt
echo 'execute make'
make
echo 'launch traefik proxy server'
sudo nohup ./traefik --configFile=traefik.toml &> /dev/null &
echo 'launch server'
nohup uvicorn main:app  --host 0.0.0.0 &>/dev/null &


