sudo apt-get install -y git python python-pip gcc python-dev python-setuptools libffi-dev
sudo apt-get install -y redis-server
git clone git@bitbucket.org:hackillinois/hackillinois-website.git
cd hackillinois-website/backend_tasks
sudo pip install -r dependencies.txt
sudo pip install googledatastore
