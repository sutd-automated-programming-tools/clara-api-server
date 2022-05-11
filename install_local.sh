
echo 'apt update'
sudo apt update
echo 'get build libraries'
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev libgdbm-dev libnss3-dev libedit-dev libc6-dev
echo 'install python3.7'
wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
sudo tar xzf Python-3.7.4.tgz
cd Python-3.7.4
sudo ./configure --enable-optimizations  -with-lto  --with-pydebug
sudo make altinstall
cd ..
echo 'removing python downloads'

sudo rm -rf Python-3.7.4.tgz Python-3.7.4
echo 'create virtualenv'
rm -rf venv
python3.7 -m pip install virtualenv --user
python3.7 -m virtualenv venv
. venv/bin/activate
echo 'adding path to .bashrc'
echo 'export LD_LIBRARY_PATH=/usr/lib/lp_solve/
export PATH=$PATH:/home/ismam/.local/bin'>>~/.bashrc
. ~/.bashrc
echo 'get update'
sudo apt-get update
echo 'install pip'
sudo apt-get -y install python3-pip
echo 'install aptitude'
sudo apt-get install -y aptitude
echo 'install lpsolve'
sudo aptitude install -y lp-solve liblpsolve55-dev
echo 'install pip requirements'
pip3 install -r requirements.txt
echo 'execute make'
make
